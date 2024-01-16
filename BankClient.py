from rich.console import Console
from rich.table import Table
from BankAccount import BankAccount

class BankClient:
    def __init__(self, client_id: int, name: str, account: BankAccount):
        self.client_id_number = client_id
        self.full_name = name
        self.account_owner = account
        
    def getName(self) -> str:
        return self.full_name
    
    def getClientId(self) -> int:
        return self.client_id_number
    
    def getAccount(self):
        return self.account_owner
    
    def printDetails(self):
        table = Table(title="", expand=True)
        table.add_column("Client ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Client Name", justify="center", style="magenta", no_wrap=True)
        table.add_column("Account ID", justify="center", style="cyan", no_wrap=True)

        table.add_row(
            str(self.getClientId()),
            str(self.getName()),
            str(self.account_owner)
        )

        console = Console()
        console.print(table)








