"""
Walk-forward fold harness (G2-style tooling, not a promotion gate).

Expanding window · never fit only on the decay/test block.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Fold:
    fold_id: int
    train_start: int
    train_end: int  # exclusive
    test_start: int
    test_end: int  # exclusive

    @property
    def train_n(self) -> int:
        return self.train_end - self.train_start

    @property
    def test_n(self) -> int:
        return self.test_end - self.test_start


def expanding_folds(
    n: int,
    *,
    min_train: int = 150,
    test_block: int = 80,
) -> list[Fold]:
    """
    Anchored expanding WF:
      train[0:min_train], test[min_train:min_train+test_block]
      train grows by test_block each fold; last fold may have shorter test.
    Guarantees train never equals only the test/decay window.
    """
    if n < min_train + 10:
        raise ValueError(f"n={n} too small for min_train={min_train}")
    folds: list[Fold] = []
    train_end = min_train
    fold_id = 1
    while train_end < n:
        test_start = train_end
        test_end = min(test_start + test_block, n)
        if test_end <= test_start:
            break
        # Refuse degenerate: train must be strictly before test and ≥ min_train
        if train_end < min_train:
            raise AssertionError("fit-only-on-decay guard")
        folds.append(
            Fold(
                fold_id=fold_id,
                train_start=0,
                train_end=train_end,
                test_start=test_start,
                test_end=test_end,
            )
        )
        train_end = test_end
        fold_id += 1
        if test_end >= n:
            break
    return folds


def folds_to_jsonable(folds: list[Fold]) -> list[dict]:
    return [asdict(f) | {"train_n": f.train_n, "test_n": f.test_n} for f in folds]


def assert_no_fit_only_on_decay(fold: Fold) -> None:
    """Train window must include history before the test block."""
    if fold.train_start != 0:
        raise AssertionError("expected anchored expanding train_start=0")
    if fold.train_end <= fold.train_start:
        raise AssertionError("empty train")
    if fold.test_start < fold.train_end:
        raise AssertionError("train/test overlap")
    if fold.train_n < 50:
        raise AssertionError("train too small — risk of decay-only fit")
