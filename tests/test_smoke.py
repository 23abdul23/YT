from ytauto.config import load


def test_config_loads_budget_cap():
    assert load("budgets")["month_cap_usd"] == 25.0
