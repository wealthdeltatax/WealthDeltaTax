"""
welfare_core.py — compatibility shim
=====================================
This module previously contained the WFR primitive layer.  It has been
merged into wfr_core.py.  This shim re-exports every public name so that
any existing import sites continue to work without modification.
"""
from wfr_core import (
    load_params,
    make_scenario_sequence,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
    make_empirical_distribution_for_start,
    make_empirical_distribution,
    make_idealised_distribution,
    ReturnDistribution,
    TaxResult,
    tax_consumption,
    tax_income,
    tax_cgt,
    tax_stock_wealth,
    tax_symmetric_flat,
    get_tax_fn,
    SYSTEM_LABELS,
    crra_utility,
    expected_utility,
    expected_tax,
    consumption_equiv_welfare,
    variance_of_consumption,
    solve_revenue_equivalent_rate,
    solve_all_rates,
    SystemResult,
    run_welfare_comparison,
    print_welfare_table,
    dm_test,
    ProgressiveRateFunction,
    tax_progressive_wdt,
    expected_utility_progressive,
    expected_tax_progressive,
    variance_progressive,
    module_output_dir,
    TOML_PATH,
    OUTPUT_ROOT,
)

__all__ = [
    'load_params', 'make_scenario_sequence',
    'make_empirical_distribution_scenario', 'make_idealised_distribution_scenario',
    'make_empirical_distribution_for_start', 'make_empirical_distribution',
    'make_idealised_distribution', 'ReturnDistribution', 'TaxResult',
    'tax_consumption', 'tax_income', 'tax_cgt', 'tax_stock_wealth',
    'tax_symmetric_flat', 'get_tax_fn', 'SYSTEM_LABELS', 'crra_utility',
    'expected_utility', 'expected_tax', 'consumption_equiv_welfare',
    'variance_of_consumption', 'solve_revenue_equivalent_rate', 'solve_all_rates',
    'SystemResult', 'run_welfare_comparison', 'print_welfare_table', 'dm_test',
    'ProgressiveRateFunction', 'tax_progressive_wdt',
    'expected_utility_progressive', 'expected_tax_progressive',
    'variance_progressive', 'module_output_dir', 'TOML_PATH', 'OUTPUT_ROOT',
]
