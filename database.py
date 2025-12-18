from product import Product
from member import Member, SilverMember, GoldMember, PlatinumMember
from coupon import Coupon, PercentDiscountCoupon, FixedDiscountCoupon
from datetime import datetime


class ProductDatabase:
    SAVE_PATH = "db-data/updated_inventory.csv"

    def __init__(self, inventory_path: str):
        # TODO: Implement this method
        self.inventory_path = inventory_path
        self.products = {}
        with open(inventory_path, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                line = line.split(",")
                barcode, name, price, quantity = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip()
                product = Product(numeric_barcode = barcode, name = name, price = float(price), quantity = int(quantity))
                self.products[barcode] = product


    def get_product(self, numeric_barcode: str) -> Product:
        """Given a barcode, return the Product object associated with that\
        barcode.

        Args:
            numeric_barcode (str): 12 digit numeric barcode
        Returns:
            Product with barcode (None if not found)
        """
        if numeric_barcode not in self.products:
            return None
        return self.products[numeric_barcode]
        

    def decrement_inventory(self, numeric_barcode: str, quantity: int):
        """Given a barcode and a quantity to decrease by, decrement the inventory of the product associated with that barcode by the quantity.

        Args:
            numeric_barcode (str): _description_
            quantity (int): _description_
        """
        if numeric_barcode not in self.products:
            return
        self.products[numeric_barcode].decrease_quantity(quantity)
        return

    def save_inventory(self):
        """Save the inventory to a CSV file"""
        with open(self.SAVE_PATH, 'w') as f:
            f.write('numeric_barcode,name,price,quantity\n')
            for product in self.products.values():
                f.write(f"{product.get_barcode()},{product.get_name()},{product.get_price()},{product.get_quantity()}\n")

class MemberDatabase:
    SAVE_PATH = "db-data/updated_memberships.csv"

    def __init__(self, membership_path: str):
        self.membership_path = membership_path
        self.membership = {}
        with open(membership_path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                line = line.split(',')
                barcode, name, tier, points = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip()
                if tier == "Silver":
                    member = SilverMember(
                        numeric_barcode = barcode,
                        name = name,
                        points = points
                    )
                elif tier == "Gold":
                    member = GoldMember(
                        numeric_barcode = barcode,
                        name = name,
                        points = points
                    )
                elif tier == "Platinum":
                    member = PlatinumMember(
                        numeric_barcode = barcode,
                        name = name,
                        points = points
                    )
                else:
                    continue
                self.membership[barcode] = member

    def get_member(self, numeric_barcode: str) -> Member:
        """Given a barcode, assert that the member is registered, and if so, return the Member object associated with that barcode.
        Args:
            numeric_barcode (str): The barcode of the member to check.

        Returns:
            Member: The Member object associated with the barcode. (None if not associated with a member)
        """
        if numeric_barcode in self.membership:
            return self.membership[numeric_barcode]
        else:
            return None

    def add_points(self, numeric_barcode: str, points: float):
        """Given a barcode, add the specified number of points to the member associated with that barcode.

        Args:
            numeric_barcode (str): The barcode of the member to add points to.
            points (int): The number of points to add.
        """
        if numeric_barcode not in self.membership:
            return
        self.membership[numeric_barcode].add_points(float(points))

    def save_memberships(self):
        """Save the current membership list to a CSV file"""
        with open(self.SAVE_PATH, "w") as f:
            f.write('numeric_barcode,name,tier,points\n')
            for member in self.membership.values():
                f.write(f"{member.get_barcode()},{member.get_name()},{member.return_membership_type()},{member.get_points()}\n")


class CouponDatabase:
    def __init__(self, coupon_path: str):
        self.coupon = {}
        with open(coupon_path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                line = line.split(',')
                barcode, expiration_date, discount_type, discount, min_purchase, description\
                 = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip(), line[5].strip()
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                discount = float(discount)
                min_purchase = float(min_purchase)
                if discount_type.lower() == "percent":
                    coupon_object = PercentDiscountCoupon(
                        numeric_barcode = barcode,
                        expiration_date = expiration_date,
                        min_purchase = min_purchase,
                        description = description,
                        percent_value = discount
                    )
                elif discount_type.lower() == "fixed":
                    coupon_object = FixedDiscountCoupon(
                        numeric_barcode = barcode,
                        expiration_date = expiration_date,
                        min_purchase = min_purchase,
                        description = description,
                        fixed_value = discount
                    )
                else:
                    continue
                self.coupon[barcode] = coupon_object

    def get_coupon(self, numeric_barcode: str) -> Coupon:
        """Given a barcode, return the Coupon object associated with that barcode."""
        if numeric_barcode in self.coupon:
            return self.coupon[numeric_barcode]
        return None
