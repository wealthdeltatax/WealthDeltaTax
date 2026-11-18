"""R9 and the budgets of architecture.md 6.1, read from the fenced `budgets` block."""

def test_block_sums_equal_the_stated_totals(R):
    rows, stated = R.budgets()
    assert (sum(r[1] for r in rows), sum(r[2] for r in rows)) == stated

def test_output_layer_smaller_than_core_plus_runner(R):
    b = {f: c for f, c, _ in R.budgets()[0]}
    assert sum(c for f, c in b.items() if f.startswith('out/')) < sum(c for f, c in b.items() if f.startswith(('core/', 'runner/')))

def test_every_file_within_budget(R):
    assert R.budget_errors(R.MODEL, R.TESTS) == []
