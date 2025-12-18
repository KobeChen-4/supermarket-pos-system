class Product:
    def __init__(
        self, numeric_barcode: str, name: str, price: float, quantity: int
    ):

        self.numeric_barcode = numeric_barcode
        self.name = name
        self.price = price
        self.quantity = quantity

    def decrease_quantity(self, quantity: int):
        """Decrease the quantity of the product by the specified quantity.

        Args:
            quantity (int): The quantity to decrease by.
        """

        self.quantity -= quantity
        return

    def is_in_stock(self) -> bool:
        """Check if the quantity of the product is greater than 0.

        Returns:
            bool: True if the product is in stock, False otherwise.
        """

        return self.quantity > 0

    def get_barcode(self) -> str:
        """Get the barcode of the product.

        Returns:
            str: The barcode of the product.
        """
        return self.numeric_barcode

    def get_name(self) -> str:
        """Get the name of the product.

        Returns:
            str: The name of the product.
        """
        return self.name

    def get_price(self) -> float:
        """Get the price of the product.

        Returns:
            float: The price of the product.
        """
        return self.price

    def get_quantity(self) -> int:
        """Get the quantity of the product.

        Returns:
            int: The quantity of the product.
        """
        return self.quantity
