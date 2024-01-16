from rich.console import Console
from rich.table import Table

class BankAccount:
    def __init__(self, account_id: int, initial_deposit: float, initial_rate: float):
        self.account_id_number = account_id
        self.balance = initial_deposit  
        self.interest = initial_rate

    def getBalance(self) -> float:
        return self.balance

    def getInterestRate(self) -> float:
        return self.interest

    def getAccountIdNumber(self) -> int:
        return self.account_id_number

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            print(f"\nDeposited ${amount}. New balance: ${self.balance}\n")
        else:
            print("Invalid deposit amount. Please enter a positive value.")

    def withdraw(self, amount: float) -> None:
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"\nWithdraw ${amount}. New balance: ${self.balance}\n")
        else:
            print("Invalid withdrawal amount. Please enter a positive value and make sure you have sufficient funds.")
            
    def printDetails(self):
        table = Table(title="", expand=True)
        table.add_column("Account ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Account Balance", justify="center", style="magenta", no_wrap=True)
        table.add_column("Interest Rate", justify="center", style="green", no_wrap=True)

        table.add_row(
            str(self.getAccountIdNumber()),
            f"₱{self.getBalance()}",
            str(self.getInterestRate()),
        )

        console = Console()
        console.print(table)
        
    

