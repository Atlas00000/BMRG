"""
L3/L4 simulation hooks (not live).

L3 outranks L2: when halted / f=0, WOULD_SKIP is irrelevant — no new entries.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class SimState:
    halted: bool = False
    f_mult: float = 1.0
    reason: str = "OK"
    l3_trips: list[str] | None = None

    def __post_init__(self) -> None:
        if self.l3_trips is None:
            self.l3_trips = []


def simulate_l3_l4(
    *,
    w250_ef_pp: float | None,
    w250_e_n: float | None,
    maxdd_pp: float,
    dd_limit_pp: float = 25.0,
    fires_90d: int | None,
    baseline_fires_90d: int = 60,
    leak_pp: float = 2.2,
    leak_baseline_pp: float = 2.2,
) -> SimState:
    """
    Guardrails (sim):
      - MaxDD >= 0.8 * DD_limit → de-risk f (halve)
      - MaxDD >= DD_limit → halt
      - Below-frontier (E_N<=0 on W250) → f=0
      - FREQUENCY_STALL (fires_90d < 50% baseline) → warn (not auto-halt in INF)
      - cost-drift Leak > 1.5x → halt flag
    """
    st = SimState()
    if w250_e_n is not None and w250_e_n <= 0:
        st.f_mult = 0.0
        st.halted = True
        st.reason = "BELOW_FRONTIER"
        st.l3_trips.append("BelowFrontier_f0")
    if maxdd_pp >= dd_limit_pp:
        st.halted = True
        st.f_mult = 0.0
        st.reason = "MAXDD_HALT"
        st.l3_trips.append("MaxDD_halt")
    elif maxdd_pp >= 0.8 * dd_limit_pp:
        st.f_mult = min(st.f_mult, 0.5)
        st.l3_trips.append("MaxDD_derisk")
        if st.reason == "OK":
            st.reason = "MAXDD_DERISK"
    if fires_90d is not None and fires_90d < 0.5 * baseline_fires_90d:
        st.l3_trips.append("FREQUENCY_STALL_warn")
        if st.reason == "OK":
            st.reason = "FREQUENCY_STALL_WARN"
    if leak_pp > 1.5 * leak_baseline_pp:
        st.halted = True
        st.f_mult = 0.0
        st.reason = "COST_DRIFT_HALT"
        st.l3_trips.append("CostDrift_halt")

    # L4 lifecycle recommendation (does not override L3 halt)
    if st.halted:
        pass
    elif w250_ef_pp is not None and w250_e_n is not None:
        if w250_e_n <= 0:
            st.f_mult = 0.0
        elif w250_ef_pp <= 0:
            st.f_mult = min(st.f_mult, 0.25)
    return st


def apply_l3_over_l2(decision: str, sim: SimState) -> dict:
    """
    When L3 halted, intelligence skip is moot — entry withheld by halt, not by L2.
    """
    if sim.halted or sim.f_mult <= 0:
        return {
            "final_action": "HALT_NO_ENTRY",
            "l2_decision": decision,
            "l2_effective": False,
            "l3_outranks": True,
            "f_mult": 0.0,
            "reason": sim.reason,
        }
    if decision == "WOULD_SKIP":
        return {
            "final_action": "SKIP",
            "l2_decision": decision,
            "l2_effective": True,
            "l3_outranks": False,
            "f_mult": sim.f_mult,
            "reason": "L2_SKIP",
        }
    return {
        "final_action": "FIRE",
        "l2_decision": decision,
        "l2_effective": True,
        "l3_outranks": False,
        "f_mult": sim.f_mult,
        "reason": "ALLOW",
    }


def sim_to_dict(sim: SimState) -> dict:
    return asdict(sim)
