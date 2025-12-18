import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cart import ShoppingCart
from product import Product
from member import PlatinumMember
from coupon import FixedDiscountCoupon


def test_cart_subtotal_equals_total_without_discounts():
    cart = ShoppingCart()
    cart.add_item(Product("random_barcode", "Milk", 2, 150))
    cart.add_item(Product("random_barcode2", "Bread", 3, 80))

    assert cart.calculate_subtotal() == 5
    assert cart.calculate_total() == 5


def test_platinum_membership_applies_discount():
    cart = ShoppingCart()
    cart.add_item(Product("random_barcode", "Milk", 2, 150))
    cart.add_item(Product("random_barcode2", "Bread", 3, 80))

    sm = PlatinumMember("random_barcode3", "John", 0)
    cart.add_membership(sm)

    assert cart.calculate_total() == 4.5


def test_fixed_discount_coupon_applies_and_does_not_duplicate():
    cart = ShoppingCart()
    cart.add_item(Product("random_barcode", "Milk", 2, 150))
    cart.add_item(Product("random_barcode2", "Bread", 3, 80))

    sm = PlatinumMember("random_barcode3", "John", 0)
    cart.add_membership(sm)
    assert cart.calculate_total() == 4.5

    fc = FixedDiscountCoupon("b4", datetime(2030, 1, 1), 1, "desc", 1)
    cart.add_coupon(fc)
    assert cart.calculate_total() == 3.5

    cart.add_coupon(fc)
    assert len(cart.get_coupons()) == 1

    assert len(cart.get_items()) == 2
