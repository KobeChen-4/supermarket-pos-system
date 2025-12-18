class Member:
    """A member of the store."""

    points_multiplier = 1  # 1 point per dollar
    discount_rate = 0  # no discount

    def __init__(self, numeric_barcode: str, name: str, points: float):
        self.barcode = numeric_barcode
        self.name = name
        self.points = float(points)

    def add_points(self, points: float):
        """Add the specified number of points to the member.

        Args:
            points (int): The number of points to add.
        """
        self.points += points

    def get_name(self) -> str:
        """Get the name of the member.

        Returns:
            str: The name of the member.
        """
        return self.name

    def get_points(self) -> int:
        """Get the number of points the member has.

        Returns:
            int: The number of points the member has.
        """
        return self.points

    def get_barcode(self) -> str:
        """Get the barcode of the member.

        Returns:
            str: The barcode of the member.
        """
        return self.barcode

    def get_points_multiplier(self) -> int:
        """Get the points multiplier for the member.

        Returns:
            int: The points multiplier for the member.
        """
        return self.points_multiplier

    def get_discount_rate(self) -> float:
        """Get the discount rate for the member.

        Returns:
            float: The discount rate for the member.
        """
        return self.discount_rate

    def return_membership_type(self) -> str:
        """Return the membership type of the member.

        Returns:
            str: The membership type of the member.
        """
        pass


class SilverMember(Member):
    """A standard member of the store."""
    points_multiplier = 1.1 
    discount_rate = 0.01

    def return_membership_type(self) -> str:
        """Return the membership type of the member.

        Returns:
            str: The membership type of the member.
        """
        return "Silver"


class GoldMember(Member):
    """A gold member of the store."""
    points_multiplier = 1.5
    discount_rate = 0.05

    def return_membership_type(self) -> str:
        """Return the membership type of the member.

        Returns:
            str: The membership type of the member.
        """
        return "Gold"


class PlatinumMember(Member):
    """A platinum member of the store."""
    points_multiplier = 2.0
    discount_rate = 0.10  

    def return_membership_type(self) -> str:
        """Return the membership type of the member.

        Returns:
            str: The membership type of the member.
        """
        return "Platinum"