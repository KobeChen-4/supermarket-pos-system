class BarcodeProcessor:
    LEFT_SIDE_MODULES = {
        "0001101": "0",
        "0011001": "1",
        "0010011": "2",
        "0111101": "3",
        "0100011": "4",
        "0110001": "5",
        "0101111": "6",
        "0111011": "7",
        "0110111": "8",
        "0001011": "9",
    } 

    RIGHT_SIDE_MODULES = {
        "1110010": "0",
        "1100110": "1",
        "1101100": "2",
        "1000010": "3",
        "1011100": "4",
        "1001110": "5",
        "1010000": "6",
        "1000100": "7",
        "1001000": "8",
        "1110100": "9",
    } 

    GUARDS = {"LEFT": "101", "CENTER": "01010", "RIGHT": "101"}

    BARCODE_LENGTH = 95
    LEFT_GUARD_LENGTH = RIGHT_GUARD_LENGTH = 3
    NUMBER_OF_MODULES = 6
    MODULE_WIDTH = 7
    CENTER_GUARD_LENGTH = 5

    def invert_barcode(self, binary_barcode: str) -> str:
        """Given a barcode (length 95 string), invert it.

        Args:
            binary_barcode (str): The barcode to invert.
        Returns:
            str: The inverted barcode.
        """

        return binary_barcode[::-1]

    def _validate_length(self, binary_barcode: str) -> bool:
        """Given a barcode (length 95 string), validate it.
        Checks for 95 length
        """

        if not len(binary_barcode) == self.BARCODE_LENGTH:
            raise ValueError("Wrong length")
        return True

    def _validate_left_guard(self, binary_barcode: str) -> bool:
        """Given a barcode, validate it.
        Correct left guard pattern.

        """

        if not binary_barcode[0:3] == self.GUARDS["LEFT"]:
            raise ValueError("Wrong LEFT guard")
        return True

    def _validate_right_guard(self, binary_barcode: str) -> bool:
        """Given a barcode, validate it.
        Correct right guard pattern

        """

        if not binary_barcode[-3:] == self.GUARDS["RIGHT"]:
            raise ValueError("Wrong RIGHT guard")
        return True

    def _validate_center_guard(self, binary_barcode: str) -> bool:
        """Given a barcode, validate it.
        Correct center guard pattern

        """

        if not binary_barcode[45:50] == self.GUARDS["CENTER"]:
            raise ValueError("Wrong CENTER guard")
        return True

    def _get_left_modules(self, binary_barcode: str) -> list[str]:
        """Given a barcode (length 95 string), get the left modules.

        Args:
            binary_barcode (str): The barcode to get the left modules from.
        Returns:
            list[str]: The left modules, each module is a length 7 string.
        """

        return [binary_barcode[i:i+7] for i in range(3, 45, 7)]

    def _get_right_modules(self, binary_barcode: str) -> list[str]:
        """Given a barcode (length 95 string), get the right modules.

        Args:
            binary_barcode (str): The barcode to get the right modules from.
        Returns:
            list[str]: The right modules, each module is a length 7 string.
        """

        return [binary_barcode[i:i+7] for i in range(50, 92, 7)]

    def _validate_modules(self, binary_barcode, module="LEFT") -> bool:
        """Given a barcode (length 95 string), validate the modules.

        Args:
            binary_barcode (str): The barcode to validate.
            module (str, optional): The module to validate. Defaults to "LEFT".

        Raises:
            ValueError: Wrong number of modules
            ValueError: Wrong length within module
            ValueError: Wrong number of ones in module
            ValueError: Wrong start or end in module

        Returns:
            bool: True if the modules are valid, Raising an error otherwise.
        """

   
        if module == "LEFT":
            modules = self._get_left_modules(binary_barcode)
            if not len(modules) == self.NUMBER_OF_MODULES:
                raise ValueError("Wrong number of LEFT modules")
            if not all(len(m) == self.MODULE_WIDTH for m in modules):
                raise ValueError("Wrong length within LEFT module")
            if not all(m.count("1") % 2 == 1 for m in modules):
                raise ValueError("Wrong number of ones in LEFT module")
            if any(m[0] == "1" for m in modules) or any(m[-1] == "0" for m in modules):
                raise ValueError("Wrong start or end in LEFT module")
        if module == "RIGHT":
            modules = self._get_right_modules(binary_barcode)
            if not len(modules) == self.NUMBER_OF_MODULES:
                raise ValueError("Wrong number of RIGHT modules")
            if not all(len(m) == self.MODULE_WIDTH for m in modules):
                raise ValueError("Wrong length within RIGHT module")
            if not all(m.count("1") % 2 == 0 for m in modules):
                raise ValueError("Wrong number of ones in RIGHT module")
            if any(m[0] == "0" for m in modules) or any(m[-1] == "1" for m in modules):
                raise ValueError("Wrong start or end in RIGHT module")
        return True

    def convert_to_12_digits(self, binary_barcode: str) -> str:
        """Given a barcode (length 95 string), convert it to 12 digits.

        Args:
            binary_barcode (str): The barcode to convert.
        Returns:
            str: The the 12 digit representation of the barcode.
        """

        left = self._get_left_modules(binary_barcode)
        right = self._get_right_modules(binary_barcode)
        if any(combination not in self.LEFT_SIDE_MODULES for combination in left) or any(combination not in self.RIGHT_SIDE_MODULES for combination in right):
            raise ValueError("Wrong binary combination")
        return "".join([self.LEFT_SIDE_MODULES[module] for module in left] + [self.RIGHT_SIDE_MODULES[module] for module in right])

    def modulo_check(self, numeric_barcode: str) -> bool:
        """Given a numeric barcode (length 12 string), check through the modulo check if it's read in properly.
        The modulo check is as follows:
            - Sum digits in odd positions (even index)
            - Sum digits in even positions (odd index)
            - Multiply the sum of the odd positions by 3
            - Add the sum of the even positions to the result
            - Take the next multiple of 10 of the result
            - Subtract the result from the next multiple of 10 of the result
            - If the result is equal to the check digit (last digit of barcode), the barcode is valid, otherwise it is invalid.

        Args:
            barcode_12 (str): The barcode to check.
        Returns:
            bool: True if the barcode is valid, Raising an error otherwise.
        """

        odd_sum = sum([int(numeric_barcode[loc]) for loc in range(0,11,2)])
        product_odd = odd_sum * 3
        even_sum = sum([int(numeric_barcode[loc]) for loc in range(1,11,2)])
        total_sum = product_odd + even_sum
        module_first = total_sum % 10
        if (10 - module_first) % 10 != int(numeric_barcode[-1]):
            raise ValueError("Security check failed")
        return True
    
    def validate_barcode(self, binary_barcode: str) -> bool:
        """Validate full UPC-A barcode structure (95-bit)."""
        self._validate_length(binary_barcode)
        self._validate_left_guard(binary_barcode)
        self._validate_right_guard(binary_barcode)
        self._validate_center_guard(binary_barcode)
        self._validate_modules(binary_barcode, module="LEFT")
        self._validate_modules(binary_barcode, module="RIGHT")
        return True

            