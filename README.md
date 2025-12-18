# Supermarket POS System (Python)

A Python-based supermarket point-of-sale (POS) system that simulates barcode scanning, shopping cart management, coupon and membership discounts, inventory tracking, and checkout processing.

This project was refactored from an academic assignment into a fully tested, modular application using **pytest**.

---

## Features

- UPC-A barcode validation and decoding
- Product, coupon, and membership barcode handling
- Shopping cart with membership and coupon discounts
- Inventory and membership database management (CSV-based)
- End-to-end POS workflow (scan → cart → checkout)
- Full test coverage using `pytest`

---

## Project Structure

supermarket_project/
├── barcode.py # Barcode validation and decoding
├── product.py # Product model
├── member.py # Membership models (Silver, Gold, Platinum)
├── coupon.py # Coupon models (Percent / Fixed)
├── database.py # Product, member, and coupon databases
├── store_backend.py # Backend interface for POS system
├── cart.py # Shopping cart logic
├── pos.py # POS system workflow
├── main.py # Example usage / entry point
├── tests/ # Pytest unit & integration tests
├── cart-data/ # Sample scanned barcode data
├── db-data/ # Sample inventory, membership, and coupon data
├── README.md
└── .gitignore

---

## Requirements

- Python 3.10+
- pytest

Install dependencies:
Install dependencies:

```bash
pip install pytest
```

---

## Running the Application
From the project root:

python main.py

This simulates scanning barcodes, building a cart, applying discounts, and checking out.

---

## Running test
All tests are implemented using pytest.

Tests cover:
    Barcode validation
    Product inventory logic
    Membership behavior
    Coupon discounts
    Database persistence
    Full POS workflow

---

## Notes
    CSV files are used to simulate persistent databases.
    Test cases isolate file I/O using temporary paths to avoid modifying source data.
    Doctests from the original coursework were refactored into standalone pytest tests.

---

## Author
Kobe Chen
Data Science @ UC San Diego