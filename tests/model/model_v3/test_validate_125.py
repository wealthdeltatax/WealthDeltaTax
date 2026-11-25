"""Brief 125c: the helper functions of the validation script on a toy case, and the script's labels."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('validate_125', ROOT / 'model' / 'studies' / 'household-arm-validation' / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def test_share_growth_gap_and_label_on_a_toy_case():
    assert v.share(25.0, 100.0) == 0.25 and abs(v.growth(100.0, 164.0) - 0.64) < 1e-12
    assert v.gap(0.5, 0.3, 0.6) == 0.0 and abs(v.gap(0.7, 0.3, 0.6) - 0.1) < 1e-12 and abs(v.gap(0.1, 0.3, 0.6) + 0.2) < 1e-12 and v.gap(0.5, 0.6, 0.3) == 0.0
    assert v.label(0.5, 0.3, 0.6, False) == 'inside' and v.label(0.7, 0.3, 0.6, False) == 'outside' and v.label(0.5, 0.3, 0.6, True) == 'definition differs'


def test_observed_ratio_reads_the_held_series():
    assert abs(v.observed_ratio(2022) - 0.05) < 1e-12 and abs(v.observed_ratio(2025) - 0.096) < 1e-12
