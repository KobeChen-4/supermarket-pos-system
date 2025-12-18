import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from product import Product


def test_product_getters_and_stock_and_decrease_quantity():
    numeric_barcode = "012345678905"
    p = Product(numeric_barcode, "Test", 10.0, 5)

    assert p.get_barcode() == numeric_barcode
    assert p.get_name() == "Test"
    assert p.get_price() == 10.0
    assert p.get_quantity() == 5

    assert p.is_in_stock() is True

    p.decrease_quantity(5)
    assert p.get_quantity() == 0
    assert p.is_in_stock() is False
