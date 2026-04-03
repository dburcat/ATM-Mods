class Account:
    """Represents a bank account with multiple named sub-accounts."""

    def __init__(self, customer_number=0, pin_number=0, checking_balance=0.0, saving_balance=0.0):
        self._customer_number = customer_number
        self._pin_number = pin_number
        # Dictionary to store account names and their balances
        self._accounts = {
            "Checking": checking_balance,
            "Savings": saving_balance
        }

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_pin_number(self):
        return self._pin_number

    def get_balance(self, account_name):
        """Get balance for a specific account."""
        return self._accounts.get(account_name, 0.0)

    def get_account_names(self):
        """Get list of all account names."""
        return list(self._accounts.keys())

    def get_total_balance(self):
        """Get sum of all account balances."""
        return sum(self._accounts.values())

    def add_account(self, account_name, initial_balance=0.0):
        """Add a new account if it doesn't already exist."""
        if account_name not in self._accounts:
            self._accounts[account_name] = initial_balance
            return True
        return False

    # ------------------------------------------------------------------
    # Balance Operation Methods
    # ------------------------------------------------------------------

    def withdraw(self, account_name, amount):
        """Withdraw funds from a specific account."""
        if account_name in self._accounts:
            if self._accounts[account_name] >= amount:
                self._accounts[account_name] -= amount
                return self._accounts[account_name]
        return None

    def deposit(self, account_name, amount):
        """Deposit funds into a specific account."""
        if account_name in self._accounts:
            self._accounts[account_name] += amount
            return self._accounts[account_name]
        return None

    def transfer(self, from_account, to_account, amount):
        """Transfer funds between two accounts."""
        if (from_account in self._accounts and 
            to_account in self._accounts and 
            self._accounts[from_account] >= amount):
            self._accounts[from_account] -= amount
            self._accounts[to_account] += amount
            return True
        return False
