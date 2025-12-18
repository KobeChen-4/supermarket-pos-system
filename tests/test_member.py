import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from member import SilverMember, GoldMember, PlatinumMember


def test_platinum_member_basic_fields_and_points():
    numeric_barcode = "012345678912"
    name = "David"
    points = 10

    m = PlatinumMember(numeric_barcode, name, points)

    assert m.get_barcode() == numeric_barcode
    assert m.get_name() == name
    assert m.get_points() == points

    assert m.get_points_multiplier() == 2
    assert m.get_discount_rate() == 0.1

    m.add_points(5)
    assert m.get_points() == 15


def test_silver_member_properties():
    numeric_barcode = "012345678912"
    name = "David"
    points = 10

    m = SilverMember(numeric_barcode, name, points)

    assert m.return_membership_type() == "Silver"
    assert m.get_points_multiplier() == 1.1
    assert m.get_discount_rate() == 0.01


def test_gold_member_properties():
    numeric_barcode = "012345678912"
    name = "David"
    points = 10

    m = GoldMember(numeric_barcode, name, points)

    assert m.return_membership_type() == "Gold"
    assert m.get_points_multiplier() == 1.5
    assert m.get_discount_rate() == 0.05


def test_platinum_member_properties():
    numeric_barcode = "012345678912"
    name = "David"
    points = 10

    m = PlatinumMember(numeric_barcode, name, points)

    assert m.return_membership_type() == "Platinum"
    assert m.get_points_multiplier() == 2
    assert m.get_discount_rate() == 0.1
