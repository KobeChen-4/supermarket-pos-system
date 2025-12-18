import sys
from pathlib import Path
import math

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pos import POSSystem
from database import ProductDatabase, MemberDatabase


def test_pos_process_barcodes_and_checkout_creates_updated_files(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]

    inventory_csv = repo_root / "db-data" / "inventory.csv"
    memberships_csv = repo_root / "db-data" / "memberships.csv"
    coupons_csv = repo_root / "db-data" / "coupons.csv"
    scan_binary = repo_root / "cart-data" / "scan_1_binary.txt"

    ProductDatabase.SAVE_PATH = str(tmp_path / "updated_inventory.csv")
    MemberDatabase.SAVE_PATH = str(tmp_path / "updated_memberships.csv")

    pos = POSSystem(str(inventory_csv), str(memberships_csv), str(coupons_csv))
    pos.process_barcodes(str(scan_binary))

    cart = pos.get_current_cart()
    items = cart.get_items()

    assert len(items) == 2
    item_names = [item.get_name() for item in items]
    assert ("Apple" in item_names) and ("Cheddar Cheese" in item_names)

    assert cart.get_membership().get_name() == "John Smith"
    assert cart.get_membership().return_membership_type() == "Gold"

    total = pos.checkout()
    assert math.isclose(total, 0.415, abs_tol=0.001)

    assert Path(MemberDatabase.SAVE_PATH).exists()
    assert Path(ProductDatabase.SAVE_PATH).exists()


def test_identify_barcode_type_matches_scan_1_txt():
    repo_root = Path(__file__).resolve().parents[1]
    scan_numeric = repo_root / "cart-data" / "scan_1.txt"

    pos = POSSystem(
        str(repo_root / "db-data" / "inventory.csv"),
        str(repo_root / "db-data" / "memberships.csv"),
        str(repo_root / "db-data" / "coupons.csv"),
    )

    expected_types = ["coupon", "membership", "product", "product"]
    calculated_types = []

    for line in scan_numeric.read_text().splitlines():
        numeric_barcode = line.strip()
        if numeric_barcode:
            calculated_types.append(pos._identify_barcode_type(numeric_barcode))

    assert calculated_types == expected_types


def test_identify_barcode_type_rejects_invalid():
    repo_root = Path(__file__).resolve().parents[1]
    pos = POSSystem(
        str(repo_root / "db-data" / "inventory.csv"),
        str(repo_root / "db-data" / "memberships.csv"),
        str(repo_root / "db-data" / "coupons.csv"),
    )

    import pytest

    with pytest.raises(ValueError, match="Invalid barcode"):
        pos._identify_barcode_type("abc")  # not 12 digits, not numeric

    with pytest.raises(ValueError, match="Invalid barcode"):
        pos._identify_barcode_type("123")  # wrong length
