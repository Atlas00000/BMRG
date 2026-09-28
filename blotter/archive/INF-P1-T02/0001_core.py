"""INF-P1-T02: create named schemas + core/raw/ops tables (v0)."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_core"
down_revision = None
branch_labels = None
depends_on = None

SCHEMAS = ("raw", "core", "features", "train", "score", "ops")


def upgrade() -> None:
    for schema in SCHEMAS:
        op.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

    op.create_table(
        "landing_file",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("bytes", sa.BigInteger(), nullable=False),
        sa.Column("source", sa.String(64), nullable=False, server_default="tester"),
        sa.Column("landed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.UniqueConstraint("sha256", name="uq_raw_landing_sha256"),
        schema="raw",
    )

    op.create_table(
        "ea_metadata",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("preset_id", sa.Text(), nullable=False),
        sa.Column("magic", sa.BigInteger(), nullable=False),
        sa.Column("ea_name", sa.Text(), nullable=False),
        sa.Column("ea_version", sa.Text(), nullable=False),
        sa.Column("designed_rr", sa.Float(), nullable=False),
        sa.Column("risk_definition", sa.Text(), nullable=False),
        sa.Column("regime_filtered", sa.Boolean(), nullable=False),
        sa.Column("baseline_frequency", sa.Float(), nullable=False),
        sa.Column("costs_defaulted", sa.JSON(), nullable=False),
        sa.Column("geometry_mode", sa.Text(), nullable=False),
        sa.Column("symbol", sa.Text(), nullable=False),
        sa.Column("timeframe", sa.Text(), nullable=False),
        sa.Column("pool_role", sa.Text(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.UniqueConstraint("preset_id", "magic", "ea_version", name="uq_core_ea_meta"),
        schema="core",
    )

    op.create_table(
        "event_manifest",
        sa.Column("event_id", sa.Text(), primary_key=True),
        sa.Column("risk_ccy", sa.Float(), nullable=False),
        sa.Column("equity_at_open", sa.Float(), nullable=False),
        sa.Column("signal_tag", sa.Text(), nullable=True),
        sa.Column("exit_reason", sa.Text(), nullable=True),
        sa.Column("magic", sa.BigInteger(), nullable=True),
        sa.Column("symbol", sa.Text(), nullable=True),
        sa.Column("side", sa.Text(), nullable=True),
        sa.Column("sl_points", sa.Float(), nullable=True),
        sa.Column("volume", sa.Float(), nullable=True),
        sa.Column("tick_value_per_point", sa.Float(), nullable=True),
        sa.Column("equity_source", sa.Text(), nullable=True),
        sa.Column("costs_defaulted", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        schema="core",
    )

    op.create_table(
        "blotter_leg",
        sa.Column("leg_id", sa.Text(), primary_key=True),
        sa.Column("event_id", sa.Text(), nullable=False),
        sa.Column("symbol", sa.Text(), nullable=False),
        sa.Column("direction", sa.Text(), nullable=False),
        sa.Column("entry_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("entry_price", sa.Float(), nullable=False),
        sa.Column("exit_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("exit_price", sa.Float(), nullable=False),
        sa.Column("initial_stop", sa.Float(), nullable=True),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.Column("pnl_gross_ccy", sa.Float(), nullable=False),
        sa.Column("cost_spread_ccy", sa.Float(), nullable=False),
        sa.Column("cost_commission_ccy", sa.Float(), nullable=False),
        sa.Column("cost_swap_ccy", sa.Float(), nullable=False),
        sa.Column("cost_slippage_ccy", sa.Float(), nullable=False),
        sa.Column("pnl_net_ccy", sa.Float(), nullable=False),
        sa.Column("exit_reason", sa.Text(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["core.event_manifest.event_id"]),
        schema="core",
    )
    op.create_index("ix_core_blotter_event_id", "blotter_leg", ["event_id"], schema="core")

    op.create_table(
        "model_version",
        sa.Column("model_semver", sa.Text(), primary_key=True),
        sa.Column("layer", sa.Text(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.Column("parent_semver", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        schema="ops",
    )

    op.create_table(
        "eval_run",
        sa.Column("run_id", sa.Text(), primary_key=True),
        sa.Column("recipe_id", sa.Text(), nullable=False),
        sa.Column("baseline_id", sa.Text(), nullable=False),
        sa.Column("scorecard_path", sa.Text(), nullable=True),
        sa.Column("verdict", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        schema="ops",
    )


def downgrade() -> None:
    op.drop_table("eval_run", schema="ops")
    op.drop_table("model_version", schema="ops")
    op.drop_index("ix_core_blotter_event_id", table_name="blotter_leg", schema="core")
    op.drop_table("blotter_leg", schema="core")
    op.drop_table("event_manifest", schema="core")
    op.drop_table("ea_metadata", schema="core")
    op.drop_table("landing_file", schema="raw")
    for schema in reversed(SCHEMAS):
        op.execute(sa.text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
