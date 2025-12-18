from pos import POSSystem


if __name__ == "__main__":
    barcode_path = "cart-data/scan_1_binary.txt"
    inventory_path = "db-data/inventory.csv"
    membership_path = "db-data/memberships.csv"
    coupon_path = "db-data/coupons.csv"

    pos = POSSystem(inventory_path, membership_path, coupon_path)

    pos.process_barcodes(
        barcode_path
    )  

    print(pos.get_current_cart())
    pos.checkout()
