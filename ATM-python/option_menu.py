from account import Account
import json
import os
import logging


class OptionMenu:
    """Handles user interaction and menu navigation for the ATM."""

    DATA_FILE = "accounts.json"
    LOG_FILE = "transactions.log"

    def __init__(self):
        self._data = {}  # dict mapping customer_number (int) -> Account
        self.logger = self._setup_logger()

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

    def _setup_logger(self):
        """Configure and return a logger for transaction logging."""
        logger = logging.getLogger('ATM')
        logger.setLevel(logging.INFO)

        # Create file handler
        fh = logging.FileHandler(self.LOG_FILE)
        fh.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - Customer %(customer_id)s - %(transaction_type)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)

        # Add handler to logger (only if not already added)
        if not logger.handlers:
            logger.addHandler(fh)

        return logger

    def log_transaction(self, customer_number, transaction_type, account_name, amount, new_balance, target_account=None):
        """Log a transaction using the logging module."""
        if transaction_type == "TRANSFER":
            message = f"TRANSFER - {amount:.2f} from {account_name} to {target_account} (Balance: {new_balance:.2f})"
        else:
            message = f"{transaction_type} - Amount: {amount:.2f} in {account_name} (New Balance: {new_balance:.2f})"
        
        # Use extra dict to pass custom fields to the formatter
        self.logger.info(
            message,
            extra={'customer_id': customer_number, 'transaction_type': transaction_type}
        )

    # ------------------------------------------------------------------
    # Main Login Flow
    # ------------------------------------------------------------------

    def get_login(self):
        while True:
            try:
                customer_number = int(input("\nEnter your customer number: "))
                pin_number = int(input("\nEnter your PIN number: "))
                if customer_number in self._data:
                    acc = self._data[customer_number]
                    if pin_number == acc.get_pin_number():
                        self.get_account_type(acc)
                        return
                print("\nWrong Customer Number or Pin Number")
            except ValueError:
                print("\nInvalid Character(s). Only Numbers.")

    # ------------------------------------------------------------------
    # Select Account Type
    # ------------------------------------------------------------------

    def get_account_type(self, acc):
        while True:
            try:
                print("\nSelect the account you want to access: ")
                account_names = acc.get_account_names()
                
                # Display all existing accounts
                for i, account_name in enumerate(account_names, 1):
                    balance = acc.get_balance(account_name)
                    print(f" Type {i} - {account_name} ({self._format_money(balance)})")
                
                # Display summary and options
                total_balance = acc.get_total_balance()
                print(f" Type {len(account_names) + 1} - View All Balances ({self._format_money(total_balance)})")
                print(f" Type {len(account_names) + 2} - View Transaction History")
                print(f" Type {len(account_names) + 3} - Create New Account")
                print(f" Type {len(account_names) + 4} - Exit")
                
                selection = int(input("\nChoice: "))
                
                if 1 <= selection <= len(account_names):
                    selected_account = account_names[selection - 1]
                    self.get_account_menu(acc, selected_account)
                elif selection == len(account_names) + 1:
                    self.view_all_balances(acc)
                elif selection == len(account_names) + 2:
                    self.view_transaction_history(acc)
                elif selection == len(account_names) + 3:
                    self.create_new_account(acc)
                elif selection == len(account_names) + 4:
                    return
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

    # ------------------------------------------------------------------
    # Account Operations Menu (Generic)
    # ------------------------------------------------------------------

    def get_account_menu(self, acc, account_name):
        """Generic account operations menu that works for any account type."""
        while True:
            try:
                balance = acc.get_balance(account_name)
                print(f"\n{account_name} Account: ")
                print(" Type 1 - View Balance")
                print(" Type 2 - Withdraw Funds")
                print(" Type 3 - Deposit Funds")
                print(" Type 4 - Transfer Funds")
                print(" Type 5 - Exit")
                
                selection = int(input("\nChoice: "))
                
                if selection == 1:
                    print(f"\n{account_name} Account Balance: {self._format_money(balance)}")
                elif selection == 2:
                    self.withdraw_funds(acc, account_name)
                elif selection == 3:
                    self.deposit_funds(acc, account_name)
                elif selection == 4:
                    self.transfer_funds(acc, account_name)
                elif selection == 5:
                    return
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

    # ------------------------------------------------------------------
    # Generic Account Operations
    # ------------------------------------------------------------------

    def withdraw_funds(self, acc, account_name):
        """Generic withdrawal from any account."""
        while True:
            balance = acc.get_balance(account_name)
            print(f"\nCurrent {account_name} Account Balance: {self._format_money(balance)}")
            amount = self._get_amount_input(f"\nAmount you want to withdraw from {account_name} Account: ")
            
            if amount is None:
                print("\nInvalid Choice.")
                continue
            
            if amount < 0:
                print("\nAmount cannot be negative.")
                continue
            
            if balance >= amount:
                new_balance = acc.withdraw(account_name, amount)
                self.log_transaction(acc._customer_number, "WITHDRAW", account_name, amount, new_balance)
                print(f"\nWithdrawal successful!")
                print(f"Current {account_name} Account Balance: {self._format_money(new_balance)}")
                break
            else:
                print("\nInsufficient funds.")

    def deposit_funds(self, acc, account_name):
        """Generic deposit to any account."""
        while True:
            balance = acc.get_balance(account_name)
            print(f"\nCurrent {account_name} Account Balance: {self._format_money(balance)}")
            amount = self._get_amount_input(f"\nAmount you want to deposit into {account_name} Account: ")
            
            if amount is None:
                print("\nInvalid Choice.")
                continue
            
            if amount < 0:
                print("\nAmount cannot be negative.")
                continue
            
            new_balance = acc.deposit(account_name, amount)
            self.log_transaction(acc._customer_number, "DEPOSIT", account_name, amount, new_balance)
            print(f"\nDeposit successful!")
            print(f"Current {account_name} Account Balance: {self._format_money(new_balance)}")
            break

    def transfer_funds(self, acc, account_name):
        """Transfer funds from one account to another."""
        while True:
            try:
                account_names = acc.get_account_names()
                available_targets = [name for name in account_names if name != account_name]
                
                if not available_targets:
                    print(f"\nNo other accounts available to transfer to.")
                    return
                
                print(f"\nSelect an account to transfer to from {account_name}:")
                for i, target_name in enumerate(available_targets, 1):
                    target_balance = acc.get_balance(target_name)
                    print(f" Type {i} - {target_name} ({self._format_money(target_balance)})")
                print(f" Type {len(available_targets) + 1} - Exit")
                
                choice = int(input("\nChoice: "))
                
                if 1 <= choice <= len(available_targets):
                    target_account = available_targets[choice - 1]
                    source_balance = acc.get_balance(account_name)
                    print(f"\nCurrent {account_name} Account Balance: {self._format_money(source_balance)}")
                    amount = self._get_amount_input(f"\nAmount you want to transfer to {target_account}: ")
                    
                    if amount is None:
                        print("\nInvalid Choice.")
                        continue
                    
                    if amount < 0:
                        print("\nAmount cannot be negative.")
                        continue
                    
                    if source_balance >= amount:
                        if acc.transfer(account_name, target_account, amount):
                            self.log_transaction(acc._customer_number, "TRANSFER", account_name, amount, acc.get_balance(account_name), target_account)
                            print(f"\nTransfer successful!")
                            print(f"Current {account_name} Account Balance: {self._format_money(acc.get_balance(account_name))}")
                            print(f"Current {target_account} Account Balance: {self._format_money(acc.get_balance(target_account))}")
                            break
                        else:
                            print("\nTransfer failed.")
                    else:
                        print("\nInsufficient funds.")
                elif choice == len(available_targets) + 1:
                    return
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

    def view_all_balances(self, acc):
        """Display all account balances."""
        print("\nYour Account Balances:")
        for account_name in acc.get_account_names():
            balance = acc.get_balance(account_name)
            print(f" {account_name}: {self._format_money(balance)}")
        print(f" Total: {self._format_money(acc.get_total_balance())}")

    def view_transaction_history(self, acc):
        """Display transaction history for the logged-in customer."""
        customer_number = acc._customer_number
        transactions = self._get_customer_transactions(customer_number)
        
        if not transactions:
            print(f"\nNo transaction history found for customer {customer_number}.")
            return
        
        print(f"\n{'='*80}")
        print(f"Transaction History for Customer {customer_number}")
        print(f"{'='*80}")
        for transaction in transactions:
            print(transaction)
        print(f"{'='*80}\n")
        
        # Pause for user to read
        input("Press Enter to continue...")

    def _get_customer_transactions(self, customer_number):
        """Read log file and return transactions for a specific customer."""
        transactions = []
        
        if not os.path.exists(self.LOG_FILE):
            return transactions
        
        try:
            with open(self.LOG_FILE, 'r') as f:
                for line in f:
                    # Check if this line contains the customer number
                    if f"Customer {customer_number}" in line:
                        # Clean up the log line for display
                        transactions.append(line.strip())
        except Exception as e:
            print(f"\nError reading transaction history: {e}")
        
        return transactions

    def create_new_account(self, acc):
        """Create a new account for the logged-in user."""
        while True:
            account_name = input("\nEnter a name for your new account: ").strip()
            
            if not account_name:
                print("\nAccount name cannot be empty.")
                continue
            
            if account_name in acc.get_account_names():
                print(f"\nAn account with the name '{account_name}' already exists.")
                continue
            
            acc.add_account(account_name, 0.0)
            print(f"\nNew account '{account_name}' created successfully!")
            break

    # ------------------------------------------------------------------
    # Create New User Account
    # ------------------------------------------------------------------

    def create_account(self):
        while True:
            try:
                cst_no = int(input("\nEnter your customer number: "))
                if cst_no not in self._data:
                    break
                print("\nThis customer number is already registered")
            except ValueError:
                print("\nInvalid Choice.")

        try:
            pin = int(input("\nEnter PIN to be registered: "))
        except ValueError:
            pin = 0

        self._data[cst_no] = Account(cst_no, pin)
        print("\nYour new account has been successfully registered!")
        print("\nRedirecting to login.............")
        self.get_login()

    # ------------------------------------------------------------------
    # JSON Persistence Methods
    # ------------------------------------------------------------------

    def save_accounts(self):
        """Save all accounts to JSON file."""
        accounts_data = {}
        for customer_number, account in self._data.items():
            accounts_data[str(customer_number)] = {
                "customer_number": account._customer_number,
                "pin_number": account._pin_number,
                "accounts": account._accounts
            }
        
        with open(self.DATA_FILE, 'w') as f:
            json.dump(accounts_data, f, indent=2)
        print(f"\nAccounts saved to {self.DATA_FILE}")

    def load_accounts(self):
        """Load all accounts from JSON file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f:
                    accounts_data = json.load(f)
                
                for customer_number_str, data in accounts_data.items():
                    customer_number = int(customer_number_str)
                    account = Account(
                        customer_number=data["customer_number"],
                        pin_number=data["pin_number"]
                    )
                    account._accounts = data["accounts"]
                    self._data[customer_number] = account
                
                print(f"\nLoaded {len(self._data)} accounts from {self.DATA_FILE}")
            except Exception as e:
                print(f"\nError loading accounts: {e}")
                print("Starting with empty account list.")
        else:
            print(f"\nNo existing account file found. Starting fresh.")

    # ------------------------------------------------------------------
    # Main Menu Entry Point
    # ------------------------------------------------------------------

    def main_menu(self):
        # Load existing accounts from JSON
        self.load_accounts()
        
        # If no accounts loaded, initialize with test accounts
        if not self._data:
            print("\nInitializing with test accounts...")
            self._data[952141] = Account(952141, 191904, 1000, 5000)
            self._data[123] = Account(123, 123, 20000, 50000)

        while True:
            try:
                print("\n Type 1 - Login")
                print(" Type 2 - Create Account")
                choice = int(input("\nChoice: "))
                if choice == 1:
                    self.get_login()
                    break
                elif choice == 2:
                    self.create_account()
                    break
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

        # Save accounts before exiting
        self.save_accounts()
        print("\nThank You for using this ATM.\n")
