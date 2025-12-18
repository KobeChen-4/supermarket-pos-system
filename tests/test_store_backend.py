import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from store_backend import StoreBackend
from database import ProductDatabase, MemberDatabase


def test_store_backend_basic_product_and_member_flow(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]

    inventory_csv = repo_root / "db-data" / "inventory.csv"
    memberships_csv = repo_root / "db-data" / "memberships.csv"
    coupons_csv = repo_root / "db-data" / "coupons.csv"

    ProductDatabase.SAVE_PATH = str(tmp_path / "updated_inventory.csv")
    MemberDatabase.SAVE_PATH = str(tmp_path / "updated_memberships.csv")

    store_backend = StoreBackend(
        str(inventory_csv),
        str(memberships_csv),
        str(coupons_csv),
    )

    assert store_backend is not None

    # product checks
    milk_barcode = "012345678905"
    milk = store_backend.get_product(milk_barcode)

    assert milk is not None
    assert milk.get_name() == "Milk"
    assert milk.get_price() == 2.99
    assert milk.get_quantity() == 150

    store_backend.decrease_product_quantity(milk, 10)
    assert milk.get_quantity() == 140

    # non-existent product
    assert store_backend.get_product("") is None

    # member checks
    jane_barcode = "257274767454"
    jane = store_backend.get_member(jane_barcode)

    assert jane is not None
    assert jane.get_points() == 1200

    store_backend.add_member_points(jane, 100)
    assert jane.get_points() == 1300
