from datetime import datetime


class Coupon:
    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
    ):
        self.numeric_barcode = numeric_barcode
        self.expiration_date = expiration_date
        self.min_purchase = min_purchase
        self.description = description

    def _is_expired(self) -> bool:
        """Check if the coupon is expired by comparing to current datetime.now()

        Returns:
            bool: True if the coupon is expired, False otherwise.
        """
        return datetime.now() > self.expiration_date

    def discount_amount(self, subtotal: float) -> float:
        """Calculate the discount amount for the coupon.
        This is a placeholder for the actual discount amount. The actual discount amount is implemented in the subclasses.

        Args:
            subtotal (float): The subtotal of the cart.
        """

        pass


class PercentDiscountCoupon(Coupon):

    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
        percent_value: float,
    ):
        super().__init__(numeric_barcode, expiration_date, min_purchase,\
 description)
        self.percent_value = percent_value

    def discount_amount(self, subtotal: float) -> float:
        """Calculates the percentage discount to subtract from the subtotal based on the coupon
        Args:
            subtotal (float): The subtotal of the cart
        Returns:
            float: The discount amount
        """

        if super()._is_expired() or subtotal < self.min_purchase:
            return 0
        return min(subtotal * (self.percent_value / 100), subtotal)

class FixedDiscountCoupon(Coupon):

    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
        fixed_value: float,
    ):
        super().__init__(
            numeric_barcode, expiration_date, min_purchase, description
        )
        self.fixed_value = fixed_value

    def discount_amount(self, subtotal: float) -> float:
        """Calculates the fixed amount to subtract from the subtotal based on the coupon

        Args:
            subtotal (float): The subtotal of the cart
        Returns:
            float: The discount amount
        """
        if super()._is_expired() or subtotal < self.min_purchase:
            return 0
        return min(self.fixed_value, subtotal)