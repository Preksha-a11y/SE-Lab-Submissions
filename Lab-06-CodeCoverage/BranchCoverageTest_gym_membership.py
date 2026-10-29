import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# =====================================================================
# Branch Coverage Tests: membership_cost
# Decision Points & Branches:
# 1. plan not in PLAN_PRICE (True / False)
# 2. age < 14 (True / False, boundary at 13 and 14)
# 3. age >= 60 (True / False, boundary at 59 and 60)
# 4. is_student (True / False when age < 60; precedence check when age >= 60)
# 5. with_trainer (True / False)
# 6. with_trainer -> plan == "yearly" (True / False)
# =====================================================================

class TestMembershipCostBranchCoverage:
    def test_branch_invalid_plan(self):
        """Branch: plan not in PLAN_PRICE -> True"""
        with pytest.raises(ValueError, match="unknown plan"):
            membership_cost("biweekly", 25, False, False)

    def test_branch_valid_plans_no_discounts(self):
        """Branch: plan not in PLAN_PRICE -> False (monthly, quarterly, yearly)"""
        assert membership_cost("monthly", 30, False, False) == 1500
        assert membership_cost("quarterly", 30, False, False) == 4000
        assert membership_cost("yearly", 30, False, False) == 12000

    def test_branch_age_boundary_too_young(self):
        """Branch: age < 14 -> True (boundary at 13)"""
        with pytest.raises(ValueError, match="too young"):
            membership_cost("monthly", 13, False, False)

    def test_branch_age_boundary_minimum_allowed(self):
        """Branch: age < 14 -> False (boundary at 14, non-student)"""
        assert membership_cost("monthly", 14, False, False) == 1500

    def test_branch_senior_discount_boundary_60(self):
        """Branch: age >= 60 -> True (boundary at 60, gets 25% discount)"""
        # 12000 - 3000 = 9000
        assert membership_cost("yearly", 60, False, False) == 9000

    def test_branch_senior_discount_above_60(self):
        """Branch: age >= 60 -> True (age 72, quarterly 4000 - 1000 = 3000)"""
        assert membership_cost("quarterly", 72, False, False) == 3000

    def test_branch_senior_with_student_flag_precedence(self):
        """Branch: age >= 60 takes precedence over is_student (both True)"""
        # Senior discount 25% is applied, student discount is bypassed in elif
        # 1500 - 375 = 1125
        assert membership_cost("monthly", 65, True, False) == 1125

    def test_branch_non_senior_boundary_59(self):
        """Branch: age >= 60 -> False (boundary at 59, non-student)"""
        assert membership_cost("monthly", 59, False, False) == 1500

    def test_branch_student_discount(self):
        """Branch: is_student -> True (age < 60, gets 10% discount)"""
        # 4000 - 400 = 3600
        assert membership_cost("quarterly", 21, True, False) == 3600

    def test_branch_non_student_regular(self):
        """Branch: is_student -> False (age < 60, no discount)"""
        assert membership_cost("quarterly", 25, False, False) == 4000

    def test_branch_with_trainer_non_yearly(self):
        """Branch: with_trainer -> True, plan == 'yearly' -> False (adds 2000)"""
        # 1500 + 2000 = 3500
        assert membership_cost("monthly", 30, False, True) == 3500
        # 4000 + 2000 = 6000
        assert membership_cost("quarterly", 30, False, True) == 6000

    def test_branch_with_trainer_yearly(self):
        """Branch: with_trainer -> True, plan == 'yearly' -> True (adds 2000, subtracts 500)"""
        # 12000 + 2000 - 500 = 13500
        assert membership_cost("yearly", 30, False, True) == 13500

    def test_branch_with_trainer_senior_yearly(self):
        """Combined Branches: Senior + Yearly + Trainer"""
        # (12000 - 3000) + 2000 - 500 = 10500
        assert membership_cost("yearly", 65, False, True) == 10500


# =====================================================================
# Branch Coverage Tests: can_enter
# Decision Points & Branches:
# 1. not plan_active (True / False)
# 2. hour < 5 or hour > 22 (Condition 1 True, Condition 2 True, Both False)
# 3. is_women_only_slot (True / False)
# 4. gender == "F" (True / False)
# =====================================================================

class TestCanEnterBranchCoverage:
    def test_branch_plan_inactive(self):
        """Branch: not plan_active -> True"""
        assert can_enter(12, False, False, "M") is False
        assert can_enter(12, False, True, "F") is False

    def test_branch_hour_under_5(self):
        """Branch: hour < 5 -> True (boundary: hour 4)"""
        assert can_enter(4, True, False, "M") is False

    def test_branch_hour_over_22(self):
        """Branch: hour > 22 -> True (boundary: hour 23)"""
        assert can_enter(23, True, False, "M") is False

    def test_branch_hour_boundary_opening_5(self):
        """Branch: 5 <= hour <= 22 -> True (boundary: hour 5 opening)"""
        assert can_enter(5, True, False, "M") is True

    def test_branch_hour_boundary_closing_22(self):
        """Branch: 5 <= hour <= 22 -> True (boundary: hour 22 closing)"""
        assert can_enter(22, True, False, "M") is True

    def test_branch_women_only_slot_female(self):
        """Branch: is_women_only_slot -> True, gender == 'F' -> True"""
        assert can_enter(11, True, True, "F") is True

    def test_branch_women_only_slot_male(self):
        """Branch: is_women_only_slot -> True, gender == 'F' -> False (Male)"""
        assert can_enter(11, True, True, "M") is False

    def test_branch_women_only_slot_non_female(self):
        """Branch: is_women_only_slot -> True, gender == 'F' -> False (Other)"""
        assert can_enter(11, True, True, "O") is False

    def test_branch_regular_slot_male_and_female(self):
        """Branch: is_women_only_slot -> False"""
        assert can_enter(14, True, False, "M") is True
        assert can_enter(14, True, False, "F") is True


# =====================================================================
# Branch Coverage Tests: bmi_category
# Decision Points & Branches:
# 1. height_m <= 0 (True: zero & negative / False: positive)
# 2. bmi < 18.5 (True: underweight / False)
# 3. bmi < 25 (True: normal / False)
# 4. bmi < 30 (True: overweight / False: obese)
# =====================================================================

class TestBmiCategoryBranchCoverage:
    def test_branch_height_zero(self):
        """Branch: height_m <= 0 -> True (boundary zero)"""
        with pytest.raises(ValueError, match="invalid height"):
            bmi_category(60, 0)

    def test_branch_height_negative(self):
        """Branch: height_m <= 0 -> True (negative height)"""
        with pytest.raises(ValueError, match="invalid height"):
            bmi_category(60, -1.75)

    def test_branch_bmi_underweight(self):
        """Branch: bmi < 18.5 -> True"""
        # weight=40, height=2.0 -> bmi=10.0
        assert bmi_category(40, 2.0) == "underweight"

    def test_branch_bmi_underweight_boundary(self):
        """Branch: bmi just under 18.5"""
        # 18.4 * 4.0 = 73.6 kg with height 2.0m -> bmi 18.4
        assert bmi_category(73.6, 2.0) == "underweight"

    def test_branch_bmi_normal_boundary_lower(self):
        """Branch: bmi == 18.5 (not < 18.5, but < 25 -> normal)"""
        # 18.5 * 4.0 = 74.0 kg with height 2.0m -> bmi 18.5
        assert bmi_category(74.0, 2.0) == "normal"

    def test_branch_bmi_normal_mid(self):
        """Branch: 18.5 <= bmi < 25 -> True"""
        # 22.0 * 4.0 = 88.0 kg with height 2.0m -> bmi 22.0
        assert bmi_category(88.0, 2.0) == "normal"

    def test_branch_bmi_overweight_boundary_lower(self):
        """Branch: bmi == 25.0 (not < 25, but < 30 -> overweight)"""
        # 25.0 * 4.0 = 100.0 kg with height 2.0m -> bmi 25.0
        assert bmi_category(100.0, 2.0) == "overweight"

    def test_branch_bmi_overweight_mid(self):
        """Branch: 25.0 <= bmi < 30 -> True"""
        # 28.0 * 4.0 = 112.0 kg with height 2.0m -> bmi 28.0
        assert bmi_category(112.0, 2.0) == "overweight"

    def test_branch_bmi_obese_boundary_lower(self):
        """Branch: bmi == 30.0 (not < 30 -> obese)"""
        # 30.0 * 4.0 = 120.0 kg with height 2.0m -> bmi 30.0
        assert bmi_category(120.0, 2.0) == "obese"

    def test_branch_bmi_obese_high(self):
        """Branch: bmi > 30 -> obese"""
        # 36.0 * 4.0 = 144.0 kg with height 2.0m -> bmi 36.0
        assert bmi_category(144.0, 2.0) == "obese"
