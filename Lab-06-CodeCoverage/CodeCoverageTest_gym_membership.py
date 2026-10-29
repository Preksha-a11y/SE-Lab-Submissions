import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ==========================================
# Tests for membership_cost
# ==========================================

def test_membership_cost_monthly_regular():
    # Regular adult monthly plan without trainer
    assert membership_cost("monthly", 30, False, False) == 1500


def test_membership_cost_quarterly_regular():
    # Regular adult quarterly plan without trainer
    assert membership_cost("quarterly", 28, False, False) == 4000


def test_membership_cost_yearly_regular():
    # Regular adult yearly plan without trainer
    assert membership_cost("yearly", 35, False, False) == 12000


def test_membership_cost_unknown_plan():
    # Unknown plan should raise ValueError
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 25, False, False)


def test_membership_cost_too_young():
    # Age below 14 should raise ValueError
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


def test_membership_cost_senior_discount():
    # Age >= 60 gets 25% discount (cost -= cost // 4)
    # 4000 - 1000 = 3000
    assert membership_cost("quarterly", 65, False, False) == 3000


def test_membership_cost_student_discount():
    # Student discount 10% (cost -= cost // 10)
    # 1500 - 150 = 1350
    assert membership_cost("monthly", 20, True, False) == 1350


def test_membership_cost_trainer_regular_plan():
    # Monthly with trainer adds 2000
    # 1500 + 2000 = 3500
    assert membership_cost("monthly", 30, False, True) == 3500


def test_membership_cost_trainer_yearly_discount():
    # Yearly with trainer adds 2000 and subtracts 500
    # 12000 + 2000 - 500 = 13500
    assert membership_cost("yearly", 30, False, True) == 13500


# ==========================================
# Tests for can_enter
# ==========================================

def test_can_enter_plan_inactive():
    # Inactive plan cannot enter
    assert can_enter(10, False, False, "M") is False


def test_can_enter_hour_before_opening():
    # Before 05:00 cannot enter
    assert can_enter(4, True, False, "M") is False


def test_can_enter_hour_after_closing():
    # After 22:00 cannot enter
    assert can_enter(23, True, False, "M") is False


def test_can_enter_women_slot_female():
    # Women-only slot allows female
    assert can_enter(10, True, True, "F") is True


def test_can_enter_women_slot_male():
    # Women-only slot denies male
    assert can_enter(10, True, True, "M") is False


def test_can_enter_normal_slot_male():
    # Regular slot allows male
    assert can_enter(10, True, False, "M") is True


# ==========================================
# Tests for bmi_category
# ==========================================

def test_bmi_category_invalid_height():
    # Height <= 0 should raise ValueError
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, 0)


def test_bmi_category_underweight():
    # BMI < 18.5
    # 45 / (1.75 * 1.75) = 14.69
    assert bmi_category(45, 1.75) == "underweight"


def test_bmi_category_normal():
    # 18.5 <= BMI < 25
    # 65 / (1.75 * 1.75) = 21.22
    assert bmi_category(65, 1.75) == "normal"


def test_bmi_category_overweight():
    # 25 <= BMI < 30
    # 80 / (1.75 * 1.75) = 26.12
    assert bmi_category(80, 1.75) == "overweight"


def test_bmi_category_obese():
    # BMI >= 30
    # 105 / (1.75 * 1.75) = 34.28
    assert bmi_category(105, 1.75) == "obese"
