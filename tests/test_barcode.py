import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from barcode import BarcodeProcessor
from tester_student import barcode_digits2binary

def test_validate_length_raises_on_empty():
    scanner = BarcodeProcessor()
    with pytest.raises(ValueError, match="Wrong length"):
        scanner._validate_length("")


def test_validate_length_ok():
    scanner = BarcodeProcessor()
    valid_numeric = "252109613999"
    valid_binary = barcode_digits2binary(valid_numeric)
    assert scanner._validate_length(valid_binary) is True


def test_validate_guards():
    scanner = BarcodeProcessor()
    assert scanner._validate_left_guard("101" + "0" * 92) is True
    assert scanner._validate_right_guard("0" * 92 + "101") is True


def test_validate_center_guard():
    scanner = BarcodeProcessor()
    valid_numeric = "252109613999"
    valid_binary = barcode_digits2binary(valid_numeric)
    assert scanner._validate_center_guard(valid_binary) is True


def test_validate_modules_left_right():
    scanner = BarcodeProcessor()
    valid_numeric = "252109613999"
    valid_binary = barcode_digits2binary(valid_numeric)
    assert scanner._validate_modules(valid_binary, module="LEFT") is True
    assert scanner._validate_modules(valid_binary, module="RIGHT") is True


def test_validate_barcode_valid_binary():
    scanner = BarcodeProcessor()
    valid_numeric = "252109613999"
    valid_binary = barcode_digits2binary(valid_numeric)
    assert scanner.validate_barcode(valid_binary) is True


def test_modulo_check_valid_numeric():
    scanner = BarcodeProcessor()
    assert scanner.modulo_check("252109613999") is True


def test_convert_to_12_digits_round_trip():
    scanner = BarcodeProcessor()
    valid_numeric = "252109613999"
    valid_binary = barcode_digits2binary(valid_numeric)
    assert scanner.convert_to_12_digits(valid_binary) == valid_numeric


def test_modulo_check_invalid_numeric_raises():
    scanner = BarcodeProcessor()
    with pytest.raises(ValueError, match="Security check failed"):
        scanner.modulo_check("036000291439")


def test_scan_files_all_valid():
    scanner = BarcodeProcessor()

    repo_root = Path(__file__).resolve().parents[1]
    scan_bin_path = repo_root / "cart-data" / "scan_1_binary.txt"
    scan_num_path = repo_root / "cart-data" / "scan_1.txt"

    # All binary barcodes should pass full validation
    checks = []
    for line in scan_bin_path.read_text().splitlines():
        binary_barcode = line.strip()
        if binary_barcode:
            checks.append(scanner.validate_barcode(binary_barcode))
    assert all(checks)

    # All numeric barcodes should pass modulo check
    checks = []
    for line in scan_num_path.read_text().splitlines():
        numeric_barcode = line.strip()
        if numeric_barcode:
            checks.append(scanner.modulo_check(numeric_barcode))
    assert all(checks)
