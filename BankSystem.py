import datetime
import sys
import time
import mysql.connector
import os

from rich.progress import track
from rich.console import Console
from rich.table import Table
from datetime import datetime
from decimal import Decimal, InvalidOperation

from BankClient import BankClient 
from BankAccount import BankAccount

host = "localhost"
user = "root"
password = "admin"
database = "bank_system_db"

connection = mysql.connector.connect (
    host = host,
    user = user,
    password = password
)

cursor = connection.cursor()

create_database = f"create database if not exists {database}";

cursor.execute(create_database)

connection.database = database

create_table_bank_accounts = """
    create table if not exists bank_accounts (
        account_id int primary key unique not null,
        account_balance decimal(10, 2) not null default 0.00,
        account_interest_rate decimal(10, 2) default 0.00
    )
"""

cursor.execute(create_table_bank_accounts)

create_table_bank_clients = """
    create table if not exists bank_clients (
        client_id int primary key unique not null,
        client_name varchar(100) not null,
        account_id int,
        foreign key (account_id) references bank_accounts(account_id)
    )
"""

cursor.execute(create_table_bank_clients) 

create_table_transaction_details = """
    create table if not exists transaction_details (
        account_id int not null,
        deposit_count int default 0,
        withdraw_count int default 0,
        foreign key (account_id) references bank_accounts(account_id)
    )
"""

cursor.execute(create_table_transaction_details)

connection.commit()
    
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

service_fee = Decimal('30.0')

def createAccount():
    clearScreen()
    
    header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
    
    try:
        while True:
            try:
                account_id = userInput("ENTER YOUR ACCOUNT ID NUMBER")
                
                account_id_exists = "select count(*) as count from bank_accounts where account_id = %s"
                
                cursor.execute(account_id_exists, (account_id,))
                
                account_owner_id = cursor.fetchone()[0]
                
                clearScreen()
                
                header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
                refreshInput(f"ACCONUNT ID NUMBER: {str(account_id)}")
                
                if account_owner_id > 0:
                    clearScreen()
                    header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
                    errorStatement(f"Error: Account ID {account_id} is already associated with a client.")
                else:
                    break
                    
            except ValueError:
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
                errorStatement("Please enter a valid positive integer.")
                
        while True:
            try:
                initial_deposit = Decimal(userInput("ENTER YOUR INITIAL DEPOSIT"))
                
                if initial_deposit > 0:
                    new_account = BankAccount(account_id, initial_deposit, 0.0)
                    
                    insert_query = "insert into bank_accounts (account_id, account_balance, account_interest_rate) values (%s, %s, %s)"
                    
                    data = (new_account.getAccountIdNumber(), new_account.getBalance(), new_account.getInterestRate())
                    
                    cursor.execute(insert_query, data)
                    
                    insert_transaction_details = "insert into transaction_details (account_id) values (%s)"
                    
                    transaction_data = (new_account.getAccountIdNumber(),)
                    
                    cursor.execute(insert_transaction_details, transaction_data)
                    
                    clearScreen()
                
                    header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
                    refreshInput(f"ACCOUNT ID NUMBER: {str(account_id)}")
                    refreshInput(f"INITIAL DEPOSIT: {str(initial_deposit)}")
                    
                    pressAnyKeyToContinue()
                    
                    break
                else:
                    clearScreen()
                    header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
                    errorStatement("Please input a valid deposit value.")
                    refreshInput(f"ACCOUNT ID NUMBER: {str(account_id)}")
                    
            except InvalidOperation:
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ CREATING AN BANK ACCOUNT ]")
                errorStatement("Please enter a valid positive integer.")
                refreshInput(f"ACCOUNT ID NUMBER: {str(account_id)}")
                
        connection.commit()
        
        mainMenu("SUCCESSFULLY CREATED A NEW BANK ACCOUNT.")
        
    except KeyboardInterrupt:
        accountManagementMenu()
  
def createClient():
    clearScreen()
    
    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
    
    try:
        while True:
            try:
                client_id = int(userInput("ENTER YOUR CLIENT ID NUMBER"))
                
                client_id_exists = "select count(*) as count from bank_clients where client_id = %s"
                
                cursor.execute(client_id_exists, (client_id,))
                
                client_owner_id = cursor.fetchone()[0]
                
                if client_owner_id > 0: 
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                    errorStatement(f"Error: Account ID {client_id} is already associated with a client.")
                else:
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                    refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
                    break
                    
            except ValueError:
                clearScreen()
                header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                errorStatement("Please enter a valid positive integer.")
        
        while True:
            try:
                client_name = str(userInput("ENTER YOUR FULL NAME")).upper()
                
                if client_name != "":
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                    refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
                    refreshInput(f"CLIENT FULL NAME: {client_name}")
                    break
                else:
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                    errorStatement("Please enter a valid full name.")
                    refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
                
            except ValueError:
                clearScreen()
                header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                errorStatement("Please enter a valid full name.")
                refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
        
        while True:
            try:
                account_id = int(userInput("ENTER YOUR ACCOUNT ID NUMBER"))

                account_id_exists_query = "SELECT COUNT(*) FROM bank_clients WHERE account_id = %s"
                
                cursor.execute(account_id_exists_query, (account_id,))
                
                account_owner_id = cursor.fetchone()[0]

                valid_account_id_query = "SELECT account_id FROM bank_accounts"
                
                cursor.execute(valid_account_id_query)
                
                all_account_ids = [row[0] for row in cursor.fetchall()]
    
                if account_id not in all_account_ids:
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                    errorStatement("Invalid account id! Your account id is not existing. Please enter a valid id.")
                    refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
                    refreshInput(f"CLIENT FULL NAME: {client_name}")
                else:
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                    refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
                    refreshInput(f"CLIENT FULL NAME: {client_name}")
                    refreshInput(f"ACCOUNT ID NUMBER: {account_id}")    
                    pressAnyKeyToContinue()
                    break
    
            except ValueError:
                clearScreen()
                header("> CLIENT MANAGEMENT > [ CREATING AN CLIENT ACCOUNT ]")
                errorStatement("Please enter a valid positive integer.")
                refreshInput(f"CLIENT ID NUMBER: {str(client_id)}")
                refreshInput(f"CLIENT FULL NAME: {client_name}")
        
        new_client = BankClient(client_id, client_name, account_id)
        
        insert_query = "insert into bank_clients (client_id, client_name, account_id) values (%s, %s, %s)"
        data = (new_client.getClientId(), new_client.getName(), new_client.getAccount())
        
        cursor.execute(insert_query, data)
        
        connection.commit()

        mainMenu("SUCCESSFULLY CREATED A NEW CLIENT.")
    except KeyboardInterrupt:
        clientManagementMenu()
    
def findAccount():
    clearScreen()
    
    header("> ACCOUNT MANAGEMENT > [ FIND AN BANK ACCOUNT ]")
        
    try:
        while True:
            try:
                account_id = int(userInput("ENTER THE ACCOUNT ID NUMBER"))
                account_exist = "select * from bank_accounts where account_id = %s"
                cursor.execute(account_exist, (account_id,))
                account = cursor.fetchone()
                
                if account:
                    account_information = BankAccount(account[0], account[1], account[2])
                    
                    clearScreen()
                    
                    header("> ACCOUNT MANAGEMENT > [ FIND AN BANK ACCOUNT ]")
                    
                    for step in track(range(100), description="[bold green]Fetching bank client information..."):
                        time.sleep(0.01)
                        
                    console = Console()
                    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
                    table.add_row(f"[bold #06D6A0]ACCOUNT DETAILS[/bold #06D6A0]" )
                    console.print(table)
 
                    account_information.printDetails()
                    print("\n")
                    break
                else:
                    clearScreen()
                    header("> ACCOUNT MANAGEMENT > [ FIND AN BANK ACCOUNT ]")
                    errorStatement("Invalid account id! The specified account does not exist. Please enter a valid id.") 
                    
            except ValueError:  
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ FIND AN BANK ACCOUNT ]")
                errorStatement("Please enter a valid positive integer.")
        
        successfulTransaction("SUCCESSFULLY FETCHED BANK ACCOUNT.")
                
        backToPreviousMenu("PLEASE ENTER ANY KEY TO BACK IN THE ACCOUNT MANAGEMENT MENU...", "bank menu")
    except KeyboardInterrupt:
        accountManagementMenu()

def findClient():
    clearScreen()
    
    header("> CLIENT MANAGEMENT > [ FIND AN CLIENT ACCOUNT ]")
    
    try:
        while True:
            try:
                client_id = int(userInput("ENTER THE CLIENT ID NUMBER"))
        
                client_exist = "select * from bank_clients where client_id = %s"
                cursor.execute(client_exist, (client_id,))
                client = cursor.fetchone()
                
                if client:
                    client_information = BankClient(client[0], client[1], client[2])

                    client_information.printDetails()
                    
                    clearScreen()
                    
                    header("> CLIENT MANAGEMENT > [ FIND AN CLIENT ACCOUNT ]")
                    
                    for step in track(range(100), description="[bold green]Fetching bank client information..."):
                        time.sleep(0.01)
                        
                    console = Console()
                    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
                    table.add_row(f"[bold #06D6A0]CLIENT DETAILS[/bold #06D6A0]" )
                    console.print(table)

                    client_information.printDetails()
                    
                    print("\n")

                    break
                else:
                    clearScreen()
                    header("> CLIENT MANAGEMENT > [ FIND AN CLIENT ACCOUNT ]")
                    print("Invalid client id! The specified account does not exist. Please enter a valid id.")  
                    
            except ValueError: 
                clearScreen()
                header("> CLIENT MANAGEMENT > [ FIND AN CLIENT ACCOUNT ]")
                errorStatement("Please enter a valid positive integer.") 
                
        successfulTransaction("SUCCESSFULLY FETCHED CLIENT ACCOUNT.")
            
        backToPreviousMenu("PLEASE ENTER ANY KEY TO BACK IN THE CLIENT MANAGEMENT MENU...", "client menu")
    except KeyboardInterrupt:
        clientManagementMenu()
        
def findAllBankAccounts():
    clearScreen()
    
    header("> ACCOUNT MANAGEMENT > [ FIND ALL BANK ACCOUNTS ]")
    
    fetch_all_bank_accounts = "select * from bank_accounts"
    
    cursor.execute(fetch_all_bank_accounts)
    
    accounts = cursor.fetchall()
    
    for step in track(range(100), description="[bold green]Fetching all bank accounts..."):
        time.sleep(0.01)
    
    console = Console()
    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold #06D6A0]BANK ACCOUNTS[/bold #06D6A0]" )
    console.print(table)
    
    for account_data in accounts:
        account_information = BankAccount(account_data[0], account_data[1], account_data[2])
        
        account_information.printDetails()
    
    print("\n")
    
    successfulTransaction("SUCCESSFULLY FETCHED ALL THE BANK ACCOUNTS.")
    
    backToPreviousMenu("PLEASE ENTER ANY KEY TO BACK IN THE ACCOUNT MANAGEMENT MENU...", "bank menu")

def findAllBankClients():
    clearScreen()
    
    header("> ACCOUNT MANAGEMENT > [ FIND ALL BANK CLIENTS ]")
    
    
    fetch_all_bank_clients = "select * from bank_clients"
    
    cursor.execute(fetch_all_bank_clients)
    
    clients = cursor.fetchall()
    
    for step in track(range(100), description="Fethcing all bank clients..."):
        time.sleep(0.01)
    
    console = Console()
    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold #06D6A0]CLIENT ACCOUNTS[/bold #06D6A0]" )
    console.print(table)
    
    for client_data in clients:
        client_information = BankClient(client_data[0], client_data[1], client_data[2])

        client_information.printDetails()
        
    print("\n")    

    successfulTransaction("SUCCESSFULLY FETCHED ALL THE CLIENT ACCOUNTS.")
    
    backToPreviousMenu("PLEASE ENTER ANY KEY TO BACK IN THE CLIENT MANAGEMENT MENU...", "client menu")

def deposit():
    clearScreen()

    header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")

    try:
        while True:
            try:
                account_id = int(userInput("ENTER YOUR ACCOUNT ID NUMBER"))
                
                fetch_account = "select count(*) as count from bank_accounts where account_id = %s"
                cursor.execute(fetch_account, (account_id,))
                account = cursor.fetchone()[0]
                
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")
                refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                
                if account > 0:
                    fetch_balance = "select account_balance from bank_accounts where account_id = %s"
                    cursor.execute(fetch_balance, (account_id,))
                    current_balance = cursor.fetchone()[0]
                    
                    fetch_interest_rate = "select account_interest_rate from bank_accounts where account_id = %s"
                    cursor.execute(fetch_interest_rate, (account_id,))
                    current_interest_rate = cursor.fetchone()[0]
                    
                    account = BankAccount(account_id, current_balance, current_interest_rate)
                    
                    while True:
                        deposit_service_fee = Decimal('0.0')
                        deposit_amount = Decimal('0.0')
                        
                        try:
                            deposit_amount = Decimal(userInput("ENTER THE AMOUNT YOU WANT TO DEPOSIT"))
            
                            if deposit_amount > 0:
                                deposit_service_fee = Decimal('30.0')
                                account.deposit(deposit_amount - deposit_service_fee)
                                clearScreen()
                                header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")
                                refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                                refreshInput(f"INITIAL DEPOSIT: {deposit_amount}")
                                break
                            else:
                                clearScreen()
                                header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")
                                errorStatement("Please enter a valid positive integer.")
                                refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                                
                        except InvalidOperation:
                            clearScreen()
                            header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")
                            errorStatement("Please enter a valid positive integer.")
                            refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                    break
                else:
                    clearScreen()
                    header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")
                    errorStatement("Account does not exist. Please enter a valid account ID.")
            except ValueError:
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ DEPOSIT ]")
                errorStatement("Please enter a valid positive integer.")
        
        clearScreen()
        
        printTransactionReceipt("deposit", account_id, deposit_amount, account.getBalance())
        
        gain_interest_rate(account_id, current_interest_rate)
            
        update_query_account = "update bank_accounts set account_balance = %s where account_id = %s"

        insert_transaction_details = "update transaction_details set deposit_count = deposit_count + 1 where account_id = %s"

        confirmation("deposit", account_id, account.getBalance(), deposit_amount, update_query_account, insert_transaction_details)
        
    except KeyboardInterrupt:
        accountManagementMenu()

def withdraw():
    clearScreen()
    
    header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
    
    try:
        while True:
            try:
                account_id = int(userInput("ENTER YOUR ACCOUNT ID NUMBER"))
            
                account = get_query_account(account_id)
                
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                
                if account > 0:
                    current_balance = get_query_account_balance(account_id)
                    
                    fetch_interest_rate = "select account_interest_rate from bank_accounts where account_id = %s"
                    cursor.execute(fetch_interest_rate, (account_id,))
                    current_interest_rate = cursor.fetchone()[0]
                    
                    account = BankAccount(account_id, current_balance, current_interest_rate)
                    
                    while True:
                        wservice_fee = Decimal('0.0')
                        withdraw_amount = Decimal('0.0')
            
                        try:
                            withdraw_amount = Decimal(userInput("ENTER THE AMOUNT YOU WANT TO WITHDRAW"))
                            
                            if withdraw_amount > 0: 
                                if withdraw_amount <= current_balance:
                                    account.withdraw(withdraw_amount + wservice_fee)
                                    clearScreen()
                                    header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                                    refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                                    refreshInput(f"INITIAL WITHDRAW: {withdraw_amount}")
                                    break
                                else:
                                    clearScreen()
                                    header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                                    errorStatement("Insufficient balance to withdraw.")
                                    refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                            else:
                                clearScreen()
                                header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                                errorStatement("Please enter a valid positive withdrawal amount.")
                                refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                        
                        except InvalidOperation:
                            clearScreen()
                            header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                            errorStatement("Please enter a valid positive integer.")
                        
                    break
                else:
                    clearScreen()
                    header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                    errorStatement("Account does not exist. Please enter a valid account ID.")
                    refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
                
            except ValueError:
                clearScreen()
                header("> ACCOUNT MANAGEMENT > [ WITHDRAW ]")
                errorStatement("Please enter a valid positive integer.")
                refreshInput(f"ACCOUNT ID NUMBER: {account_id}")
        
        clearScreen()
        
        printTransactionReceipt("withdraw", account_id, withdraw_amount, account.getBalance())
        
        gain_interest_rate(account_id, current_interest_rate)
            
        update_query_account = "update bank_accounts set account_balance = %s where account_id = %s"

        insert_transaction_details = "update transaction_details set withdraw_count = withdraw_count + 1 where account_id = %s"
        
        confirmation("withdraw", account_id, account.getBalance(), withdraw_amount, update_query_account, insert_transaction_details)
        
    except KeyboardInterrupt:
       accountManagementMenu()
    
def accountManagementMenu():
    clearScreen()
    
    try:
        console = Console()
        header("> [ ACCOUNT MANAGEMENT ]")
        
        while True:
            table = Table(border_style="#118AB2", expand=True, padding=1)
            table.add_column("[bold #ECFFDC]ACCOUNT MANAGEMENT[/bold #ECFFDC]", justify="center", style="green")
            table.add_row(f"[bold #ECFFDC][ 1 ] CREATE NEW BANK ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 2 ] LIST ALL BANK ACCOUNTS[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 3 ] FIND AN BANK ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 4 ] DEPOSIT TO AN BANK ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 5 ] WITHDRAW TO AN BANK ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #EF476F][ 6 ] RETURN TO MAIN MENU[/bold #EF476F]")
            console.print(table)
        
            try:
                choice = int(userInput("PLEASE ENTER YOUR CHOICE"))
                
                if choice > 0 and choice <= 6:
                    break;
                else:
                    clearScreen()
                    header("> [ ACCOUNT MANAGEMENT ]")
                    errorStatement("Please enter a valid choice between 1 and 6.")
                    
            except ValueError:
                clearScreen()
                header("> [ ACCOUNT MANAGEMENT ]")
                errorStatement("Please enter a valid integer value.")
                
        if choice == 1:
            createAccount()
        elif choice == 2:
            findAllBankAccounts()
        elif choice == 3:
            findAccount()
        elif choice == 4:
            deposit()
        elif choice == 5:
            withdraw()
        elif choice == 6:
            mainMenu("")
    except KeyboardInterrupt:
        mainMenu("")
    
def clientManagementMenu():    
    clearScreen()
    
    try:
        console = Console()
        header("> [ CLIENT MANAGEMENT]")
        
        while True:
            table = Table(border_style="#118AB2", expand=True, padding=1)
            table.add_column("[bold #ECFFDC]CLIENT MANAGEMENT[/bold #ECFFDC]", justify="center", style="green", header_style="bold")
            table.add_row(f"[bold #ECFFDC][ 1 ] CREATE NEW CLIENT ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 2 ] LIST ALL CLIENT ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 3 ] FIND AN CLIENT ACCOUNT[/bold #ECFFDC]")
            table.add_row(f"[bold #EF476F][ 4 ] RETURN TO MAIN MENU[/bold #EF476F]")
            console.print(table)
        
            try:
                choice = int(userInput("PLEASE ENTER YOUR CHOICE"))
                
                if choice > 0 and choice <= 4:
                    break;
                else:
                    clearScreen()
                    header("> [ CLIENT MANAGEMENT]")
                    errorStatement("Please enter a valid choice between 1 and 4")
                    
            except ValueError:
                clearScreen()
                header("> [ CLIENT MANAGEMENT]")
                errorStatement("Please enter a valid integer value")
                
        if choice == 1:
            createClient()
        elif choice == 2:
            findAllBankClients()
        elif choice == 3:
            findClient()
        elif choice == 4:
            mainMenu("")
    except KeyboardInterrupt:
        mainMenu("")

def quit():
    clearScreen()
    console = Console()
    table = Table(border_style="bold #bb9af7", expand=True, padding=2)
    table.add_column("[bold #c0caf5]PROGRAM TERMINATED[/bold #c0caf5]", justify="center", style="green", header_style="bold")
    table.add_row(f"[bold #c0caf5]PLATFORM TECHNOLOGIES[/bold #c0caf5]")
    table.add_row(f"[bold #c0caf5]INDIVIDUAL CASE STUDY[/bold #c0caf5]")
    table.add_row(f"[bold #c0caf5]THANK YOU FOR USING OUR BANK SYSTEM[/bold #c0caf5]")
    table.add_row(f"[bold #c0caf5]MUCH LOVE FROM CAPITAL GUARD FAMILY[/bold #c0caf5]")
    table.add_row(f"[bold #c0caf5]MARTIN, MARLON A.[/bold #c0caf5]")
    table.add_row(f"[bold #c0caf5]BSIT - 2C[/bold #c0caf5]")
    console.print(table)
    sys.exit(0)
        
def get_query_account(account_id: int):
    fetch_account = "select count(*) as count from bank_accounts where account_id = %s"
    cursor.execute(fetch_account, (account_id,))
    return cursor.fetchone()[0]
    
def get_query_account_balance(account_id: int):
    fetch_balance = "select account_balance from bank_accounts where account_id = %s"
    cursor.execute(fetch_balance, (account_id,))
    return cursor.fetchone()[0]

def gain_interest_rate(account_id: int, current_interest_rate: Decimal):
    fetch_deposit_count = "SELECT deposit_count FROM transaction_details WHERE account_id = %s"
    cursor.execute(fetch_deposit_count, (account_id,))
    deposit_count = cursor.fetchone()[0]
    
    interest_rate = Decimal('0.0')

    if deposit_count % 5 == 0:
        interest_rate = Decimal('1.0')
    else:
        interest_rate = Decimal('0.0')
        
    current_interest_rate += interest_rate

    update_query_account = "UPDATE bank_accounts SET account_interest_rate = %s WHERE account_id = %s"
    cursor.execute(update_query_account, (current_interest_rate, account_id))

    connection.commit()
    
def clearScreen():
    return os.system('cls')

def errorStatement(text: str):
    console = Console()
    
    table = Table(border_style="bold #EF476F", expand=True)
    table.add_column("[bold #EF476F]ERROR HANDLERS[/bold #EF476F]", justify="center", style="red", header_style="bold")
    table.add_row(f"[white]{text}[/white]")
    console.print(table)
    
def successfulTransaction(text: str):   
    console = Console()
    
    table = Table(border_style="bold #A1FF4A", expand=True)
    table.add_column("[bold #A1FF4A]TRANSACTION SUCCESSFULL[/bold #A1FF4A]", justify="center", style="#A1FF4A", header_style="bold")
    table.add_row(f"[white]{text}[/white]")
    console.print(table)

def backToPreviousMenu(text: str, navigate: str):
    console = Console()
    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold #06D6A0]{text}[/bold #06D6A0]" )
    console.print(table)
    
    choice = str(input(""))
    
    if choice == '':
        if navigate == 'bank menu':
            accountManagementMenu()
        elif navigate == 'client menu':
            clientManagementMenu()
            
def userInput(text: str):
    console = Console()
    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold #06D6A0]{text}[/bold #06D6A0]" )
    console.print(table)
                
    choice = input("> "+"")

    return choice

    
def printTransactionReceipt(transaction_type: str, account_id: int, transaction_amount: float, remaining_balance: float):
    header(f"> ACCOUNT MANAGEMENT > {transaction_type.upper()} > [ CONFIRMATION ]")
    
    console = Console()
    
    table = Table(border_style=f"bold white", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold white]TRANSACTION RECEIPT[/bold white]")
    console.print(table)
       
    table = Table(title="", expand=True)
    table.add_column("Account ID", justify="center", style="cyan", no_wrap=True)
    table.add_column(f"{transaction_type.capitalize()} Amount", justify="center", style="magenta")
    table.add_column("Remaining Balance", justify="center", style="green")
    table.add_column("Service Fee", justify="center", style="red")
    
    table.add_row(
            str(account_id),
            f"₱{transaction_amount:.2f}",
            str(remaining_balance),
            "₱30.00"
        )
    
    console.print(table)
    
    print("\n")
     
def confirmation(transaction: str, account_id: int, current_balance: float,  transaction_balance: Decimal,  query_update: str, transaction_update_query: str):
    while True:
        try:
            console = Console()
            table = Table(border_style="bold #06D6A0", expand=True)
            table.add_column("[bold #06D6A0]PLEASE CONFIRM YOUR TRANSACTION[/bold #06D6A0]", justify="center", style="green", header_style="bold")
            table.add_row(f"[white]Please enter 'Y' for yes and 'N' for a no.[/white]")
            console.print(table)
            
            confirm = str(input("> ")).upper()

            if confirm == 'Y':
                update_account_balance = query_update
                cursor.execute(update_account_balance, (current_balance, account_id,))
                connection.commit()
                
                clearScreen()
                
                console = Console()

                table = Table(border_style="bold #A1FF4A", expand=True)
                table.add_column("[bold #A1FF4A]TRANSACTION SUCCESSFULL[/bold #A1FF4A]", justify="center", style="green", header_style="bold")
                table.add_row(f"[orange]TRANSACTION TIME: {current_datetime}[/orange]")
                table.add_row(f"[yellow]THANK YOU FOR BANKING WITH US![/yellow]")
                console.print(table)

                choice = pressAnyKeyToContinue()

                if choice == '':
                    if transaction.lower() == "withdraw":
                        update_withdraw_count = transaction_update_query
                        cursor.execute(update_withdraw_count, (account_id,))
                        connection.commit()
                        mainMenu(f"SUCCESSFULLY WITHDRAW ₱{transaction_balance}.00 TO YOUR ACCOUNT.\n")
                        break
                    elif transaction.lower() == "deposit":
                        update_deposit_count = transaction_update_query
                        cursor.execute(update_deposit_count, (account_id,))
                        connection.commit()
                        mainMenu(f"SUCCESSFULLY DEPOSIT ₱{transaction_balance}.00 TO YOUR ACCOUNT.\n")
                        break
                else:
                    if transaction.lower() == "withdraw":
                        update_withdraw_count = transaction_update_query
                        cursor.execute(update_withdraw_count, (account_id,))
                        connection.commit()
                        mainMenu(f"SUCCESSFULLY WITHDRAW ₱{transaction_balance}.00 TO YOUR ACCOUNT.\n")
                        break
                    elif transaction.lower() == "deposit":
                        update_deposit_count = transaction_update_query
                        cursor.execute(update_deposit_count, (account_id,))
                        connection.commit()
                        mainMenu(f"SUCCESSFULLY DEPOSIT ₱{transaction_balance}.00 TO YOUR ACCOUNT.\n")
                        break
            elif confirm == 'N':
                errorStatement(f"TRANSACTION CANCELLED")
            else:
                clearScreen()
                printTransactionReceipt("", account_id, transaction_balance, current_balance)
                errorStatement("Please enter a valid string value of 'Y' or 'N.'")
        except ValueError:
            clearScreen()
            printTransactionReceipt("", account_id, transaction_balance, current_balance)
            errorStatement("Please enter a valid string value of 'Y' or 'N.'")
  
def refreshInput(text: str):
    console = Console()
    table = Table(border_style="bold green", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold green]{text}[/bold green]")
    console.print(table)

def pressAnyKeyToContinue():
    console = Console()
    table = Table(border_style="bold #06D6A0", expand=True, show_footer=False, show_header=False)
    table.add_row("[bold #06D6A0]PLEASE ENTER ANY KEY TO CONTINUE...[/bold #06D6A0]")
    console.print(table)
                
    choice = str(input(""))
                    
    if choice == "":
        return
    else:
        return

def header(navigation: str):
    console = Console()
    table = Table(border_style=f"bold #758BFD", expand=True, show_footer=False, show_header=False)
    table.add_row(f"[bold #7189FF]CAPITAL GUARD BANK {navigation}[/bold #7189FF]")
    console.print(table)

def mainMenu(status: str):
    clearScreen()
    console = Console()
    
    header("")

    if status:
        table = Table(border_style=f"bold #A1FF4A", expand=True)
        table.add_column(f"[bold #A1FF4A]NOTIFICATION[/bold #A1FF4A]", justify="center", style="green", no_wrap=True)
        table.add_row(f"[bold #A1FF4A]{status}[/bold #A1FF4A]")
        table.add_row(f"[bold #A1FF4A]TRANSACTION TIME: {current_datetime}[/bold #A1FF4A]")
        console.print(table)
    
    try:
        while True:
            table = Table(border_style="bold #118AB2", expand=True, padding=1)
            table.add_column("[bold #ECFFDC]MAIN MENU[/bold #ECFFDC]", justify="center", header_style="bold")
            table.add_row(f"[bold #ECFFDC][ 1 ] ACCOUNT MANAGEMENT[/bold #ECFFDC]")
            table.add_row(f"[bold #ECFFDC][ 2 ] CLIENT MANAGEMENT[/bold #ECFFDC ]")
            table.add_row(f"[bold #EF476F][ 3 ] QUIT[/bold #EF476F]")
            console.print(table)
        
            try:
                choice = int(userInput("PLEASE ENTER YOUR CHOICE"))
                
                if choice > 0 and choice <= 3:
                    break;
                else:
                    clearScreen()
                    errorStatement("Please enter a valid choice between 1 and 3")
                    
            except ValueError:
                clearScreen()
                errorStatement("Please enter a valid integer value")
                
        if choice == 1:
            accountManagementMenu()
        elif choice == 2:
            clientManagementMenu()
        elif choice == 3:
            quit()
    except KeyboardInterrupt:
        quit()
        
def run():
    try:
        mainMenu("")
        return True
    except Exception as e:
        errorStatement(f"[ Error compilation on main program: {e} ]")
        return False
    
def main():
    run()
    
if __name__ == '__main__':
    main()
    
    