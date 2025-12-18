import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from database import ProductDatabase, MemberDatabase, CouponDatabase
from coupon import PercentDiscountCoupon


def test_product_database_decrement_and_save(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    inventory_csv = repo_root / "db-data" / "inventory.csv"

    ProductDatabase.SAVE_PATH = str(tmp_path / "updated_inventory.csv")

    pdb = ProductDatabase(str(inventory_csv))
    milk_barcode = "012345678905"
    milk = pdb.get_product(milk_barcode)

    assert milk is not None
    assert milk.get_quantity() == 150

    pdb.decrement_inventory(milk_barcode, 10)
    assert milk.get_quantity() == 140

    pdb.save_inventory()

    pdb2 = ProductDatabase(str(inventory_csv))
    milk2 = pdb2.get_product(milk_barcode)
    assert milk2.get_quantity() == 150

    pdb3 = ProductDatabase(ProductDatabase.SAVE_PATH)
    milk3 = pdb3.get_product(milk_barcode)
    assert milk3.get_quantity() == 140


def test_member_database_add_points_and_save(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    memberships_csv = repo_root / "db-data" / "memberships.csv"

    MemberDatabase.SAVE_PATH = str(tmp_path / "updated_memberships.csv")

    mdb = MemberDatabase(str(memberships_csv))
    jane_barcode = "257274767454"
    jane = mdb.get_member(jane_barcode)

    assert jane is not None
    assert jane.get_points() == 1200

    mdb.add_points(jane_barcode, 100)
    assert jane.get_points() == 1300

    mdb.save_memberships()
    assert Path(MemberDatabase.SAVE_PATH).exists()


def test_coupon_database_loads_percent_coupon():
    repo_root = Path(__file__).resolve().parents[1]
    coupons_csv = repo_root / "db-data" / "coupons.csv"

    cdb = CouponDatabase(str(coupons_csv))
    sample_coupon_barcode = "149234073227"
    coupon = cdb.get_coupon(sample_coupon_barcode)

    assert isinstance(coupon, PercentDiscountCoupon)
