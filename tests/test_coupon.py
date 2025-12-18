import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parents[1]))

from coupon import PercentDiscountCoupon, FixedDiscountCoupon


def test_is_expired_true_for_past_date():
    barcode = "012345678925"
    expiration_date_expired = datetime(2024, 12, 31, 11, 59, 59)
    min_purchase = 20.0
    description = "This is our tester!"
    percent_value = 15.5

    c = PercentDiscountCoupon(
        barcode, expiration_date_expired, min_purchase, description, percent_value
    )
    assert c._is_expired() is True


def test_is_expired_false_for_future_date():
    barcode = "012345678925"
    expiration_date_not_expired = datetime(2025, 12, 31, 11, 59, 59)
    min_purchase = 20.0
    description = "This is our tester!"
    percent_value = 15.5

    c = PercentDiscountCoupon(
        barcode, expiration_date_not_expired, min_purchase, description, percent_value
    )
    assert c._is_expired() is False


def test_percent_discount_amount_matches_doctest():
    barcode = "012345678925"
    expiration_date_not_expired = datetime(2025, 12, 31, 11, 59, 59)
    min_purchase = 20.0
    description = "This is our tester!"
    percent_value = 15.5

    c = PercentDiscountCoupon(
        barcode, expiration_date_not_expired, min_purchase, description, percent_value
    )

    # 15.5% of 200.0 = 31.0
    assert c.discount_amount(200.0) == 31.0

    # Below min_purchase => 0
    assert c.discount_amount(15.0) == 0


def test_fixed_discount_amount_matches_doctest():
    barcode = "012345678925"
    expiration_date_not_expired = datetime(2025, 12, 31, 11, 59, 59)
    min_purchase = 20.0
    description = "This is our tester!"
    fixed_value = 30.0

    c = FixedDiscountCoupon(
        barcode, expiration_date_not_expired, min_purchase, description, fixed_value
    )

    assert c.discount_amount(200.0) == 30.0

    assert c.discount_amount(20.0) == 20.0

    assert c.discount_amount(10.0) == 0
