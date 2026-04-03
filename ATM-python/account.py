class Account:
    """Represents a bank account with checking and savings balances."""

    def __init__(self, customer_number=0, pin_number=0, checking_balance=0.0, saving_balance=0.0):
        self._customer_number = customer_number
        self._pin_number = pin_number
        self._checking_balance = checking_balance
        self._saving_balance = saving_balance
        self._balances = (checking_balance, saving_balance)

    # ------------------------------------------------------------------
    # Getters and Setters
    # ------------------------------------------------------------------

    def set_customer_number(self, customer_number):
        self._customer_number = customer_number
        return customer_number

    def get_customer_number(self):
        return self._customer_number

    def set_pin_number(self, pin_number):
        self._pin_number = pin_number
        return pin_number

    def get_pin_number(self):
        return self._pin_number

    def get_checking_balance(self):
        return self._checking_balance

    def get_saving_balance(self):
        return self._saving_balance
    
    def get_balances(self):
        return self._balances

    # ------------------------------------------------------------------
    # Balance Calculation Methods
    # ------------------------------------------------------------------

    def calc_checking_withdraw(self, amount):
        self._checking_balance -= amount
        return self._checking_balance

    def calc_saving_withdraw(self, amount):
        self._saving_balance -= amount
        return self._saving_balance

    def calc_checking_deposit(self, amount):
        self._checking_balance += amount
        return self._checking_balance

    def calc_saving_deposit(self, amount):
        self._saving_balance += amount
        return self._saving_balance

    def calc_check_transfer(self, amount):
        self._checking_balance -= amount
        self._saving_balance += amount

    def calc_saving_transfer(self, amount):
        self._saving_balance -= amount
        self._checking_balance += amount

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    @staticmethod
    def _format_money(amount):
        return "${:,.2f}".format(amount)

    @staticmethod
    def _get_amount_input(prompt):
        """Prompt the user for a monetary amount, returning a float.

        Returns None when the user enters a non-numeric value.
        """
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # User Input Methods – Checking Account
    # ------------------------------------------------------------------

    def get_checking_withdraw_input(self):
        while True:
            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
            amount = self._get_amount_input("\nAmount you want to withdraw from Checking Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._checking_balance - amount) >= 0:
                self.calc_checking_withdraw(amount)
                print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                break
            else:
                print("\nBalance Cannot be Negative.")

    def get_checking_deposit_input(self):
        while True:
            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
            amount = self._get_amount_input("\nAmount you want to deposit into Checking Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._checking_balance + amount) >= 0:
                self.calc_checking_deposit(amount)
                print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                break
            else:
                print("\nBalance Cannot Be Negative.")

    # ------------------------------------------------------------------
    # User Input Methods – Savings Account
    # ------------------------------------------------------------------

    def get_saving_withdraw_input(self):
        while True:
            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
            amount = self._get_amount_input("\nAmount you want to withdraw from Savings Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._saving_balance - amount) >= 0:
                self.calc_saving_withdraw(amount)
                print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                break
            else:
                print("\nBalance Cannot Be Negative.")

    def get_saving_deposit_input(self):
        while True:
            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
            amount = self._get_amount_input("\nAmount you want to deposit into your Savings Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._saving_balance + amount) >= 0:
                self.calc_saving_deposit(amount)
                print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                break
            else:
                print("\nBalance Cannot Be Negative.")

    # ------------------------------------------------------------------
    # Transfer Funds Between Accounts
    # ------------------------------------------------------------------

    def get_transfer_input(self, acc_type):
        while True:
            try:
                if acc_type == "Checking":
                    print("\nSelect an account you wish to transfer funds to:")
                    print("1. Savings")
                    print("2. Exit")
                    choice = int(input("\nChoice: "))
                    if choice == 1:
                        print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                        amount = self._get_amount_input("\nAmount you want to deposit into your Savings Account: ")
                        if amount is None:
                            print("\nInvalid Choice.")
                            continue
                        if amount >= 0 and (self._saving_balance + amount) >= 0 and (self._checking_balance - amount) >= 0:
                            self.calc_check_transfer(amount)
                            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                            break
                        else:
                            print("\nBalance Cannot Be Negative.")
                    elif choice == 2:
                        return
                    else:
                        print("\nInvalid Choice.")

                elif acc_type == "Savings":
                    print("\nSelect an account you wish to transfer funds to: ")
                    print("1. Checking")
                    print("2. Exit")
                    choice = int(input("\nChoice: "))
                    if choice == 1:
                        print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                        amount = self._get_amount_input("\nAmount you want to transfer to your Checking Account: ")
                        if amount is None:
                            print("\nInvalid Choice.")
                            continue
                        if amount >= 0 and (self._checking_balance + amount) >= 0 and (self._saving_balance - amount) >= 0:
                            self.calc_saving_transfer(amount)
                            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                            break
                        else:
                            print("\nBalance Cannot Be Negative.")
                    elif choice == 2:
                        return
                    else:
                        print("\nInvalid Choice.")

            except ValueError:
                print("\nInvalid Choice.")
