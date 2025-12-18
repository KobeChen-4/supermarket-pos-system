from product import Product
from member import Member, SilverMember, GoldMember, PlatinumMember
from coupon import Coupon, FixedDiscountCoupon, PercentDiscountCoupon


class ShoppingCart:
    def __init__(self):
        self.products = []
        self.membership = None
        self.coupons = {}
        

    def add_item(self, item: Product):
        """Add the specified item to the cart.

        Args:
            item (Product): The item to add to the cart.
        """
        self.products.append(item)
        return

    def add_membership(self, membership: Member):
        """Add a membership to the cart.

        Args:
            membership (Member): The membership to add to the cart.
        """
        self.membership = membership
        return

    def add_coupon(self, coupon: Coupon):
        """Add a coupon to the cart.

        Args:
            coupon (Coupon): The coupon to add to the cart.
        """
        if coupon.numeric_barcode in self.coupons:
            return
        self.coupons[coupon.numeric_barcode] = coupon

    def get_items(self) -> list[Product]:
        """Get the items in the cart.

        Returns:
            list[Product]: The items in the cart.
        """
        return self.products

    def get_membership(self) -> Member:
        """Get the membership in the cart.

        Returns:
            Member: The membership in the cart.
        """
        return self.membership

    def get_coupons(self) -> list[Coupon]:
        """Get the coupons in the cart.

        Returns:
            list[Coupon]: The coupons in the cart.
        """
        return list(self.coupons.values())

    def calculate_subtotal(self) -> float:
        """Calculate the price of all items in the cart.

        Returns:
            float: The subtotal of the cart.
        """
        return sum([float(item.get_price()) for item in self.products])

    def calculate_total(self) -> float:
        """Calculate the total price of the cart, with coupon applied and membership applicable

        Returns:
            float: The total price of the cart.
        """
        subtotal = self.calculate_subtotal()
        total_coupon_discount = sum([coupon.discount_amount(subtotal) for coupon in self.coupons.values()])
        if self.membership:
            membership_discount = subtotal * self.membership.get_discount_rate()
        else:
            membership_discount = 0
        sum_discount = total_coupon_discount + membership_discount
        total = max(subtotal - sum_discount, 0.0)
        return total