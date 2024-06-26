import time
import os
import csv

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
from rich.progress import Progress
from rich.traceback import install

from email_list_manager import EmailListManager
from campaign_manager import CampaignManager
from email_sender import EmailSender

install(show_locals=True)
email_list_manager = EmailListManager()
campaign_manager = CampaignManager()
email_sender = EmailSender(email_list_manager)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    console = Console()
    console.print("""
    $$$$$$$$\                         $$\ $$\ $$$$$$$$\ $$\                         
    $$  _____|                        \__|$$ |$$  _____|$$ |                        
    $$ |      $$$$$$\$$$$\   $$$$$$\  $$\ $$ |$$ |      $$ | $$$$$$\  $$\  $$\  $$\ 
    $$$$$\    $$  _$$  _$$\  \____$$\ $$ |$$ |$$$$$\    $$ |$$  __$$\ $$ | $$ | $$ |
    $$  __|   $$ / $$ / $$ | $$$$$$$ |$$ |$$ |$$  __|   $$ |$$ /  $$ |$$ | $$ | $$ |
    $$ |      $$ | $$ | $$ |$$  __$$ |$$ |$$ |$$ |      $$ |$$ |  $$ |$$ | $$ | $$ |
    $$$$$$$$\ $$ | $$ | $$ |\$$$$$$$ |$$ |$$ |$$ |      $$ |\$$$$$$  |\$$$$$\$$$$  |
    \________|\__| \__| \__| \_______|\__|\__|\__|      \__| \______/  \_____\____/ 
    """)

    console.print("\n[bold]Welcome to EmailFlow! Please select an option:[/bold]\n")
    console.print("1. View Email List")
    console.print("2. Add New Email")
    console.print("3. Import Email List")
    console.print("4. Create Email Campaign")
    console.print("5. Schedule Campaign and Send Emails")
    console.print("6. View Campaign Log")
    console.print("7. Exit")

    choice = input("\nEnter your choice: ")
    return choice

def view_email_list(manager):
    email_list = manager.get_email_list()
    if email_list:
        table = Table(title="Current Email List")
        table.add_column("Email Address", justify="left")
        table.add_column("Prospect / Customer Name", justify="left")
        table.add_column("User Added", justify="left")
        table.add_column("Emails Sent", justify="left")
        
        for email in email_list:
            table.add_row(
                email["Email address"],
                email["Prospect / Customer Name"],
                email["User added"],
                email["Emails sent"]
            )
        
        console = Console()
        console.print(table)
    else:
        print("Email list is empty.")
    
    input("\nPress Enter to return to the main menu.")

def add_new_email(manager):
    email = input("Enter the new email address: ")
    name = input("Enter the name of the prospect/customer: ")
    manager.add_email(email, name)
    print(f"{email} added to the email list.")
    input("\nPress Enter to return to the main menu.")

def import_email_list(manager):
    csv_path = input("Enter the path to the CSV file: ")
    emails = []
    try:
        with open(csv_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row.get("Email address")
                name = row.get("Prospect / Customer Name")
                emails.append((email, name))
        manager.import_email_list(emails)
        print("Emails imported.")
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    input("\nPress Enter to return to the main menu.")

def create_email_campaign(campaign_manager):
    name = input("Enter campaign name: ")
    subject = input("Enter campaign subject: ")
    from_email = input("Enter from email address: ")
    template_id = input("Enter email template ID: ")
    description = input("Enter campaign description: ")
    campaign = campaign_manager.create_campaign(name, subject, from_email, template_id, description)
    print(f"Campaign '{name}' created.")
    input("\nPress Enter to return to the main menu.")

def schedule_campaign(campaign_manager, manager, email_sender):
    campaign_name = input("Enter the campaign name to schedule: ")
    campaign = campaign_manager.get_campaign(campaign_name)
    if not campaign:
        print("Campaign not found. Please create the campaign first.")
    else:
        email_list = manager.get_email_list()
        if not email_list:
            print("Email list is empty. Cannot schedule campaign.")
        else:
            for entry in email_list:
                email = entry["Email address"]
                name = entry["Prospect / Customer Name"]
                email_sender.send_email(email, name, campaign)
                manager.increment_email_count(email)  # Increment email count here
            print("Campaign scheduled and emails sent.")
    input("\nPress Enter to return to the main menu.")

def send_emails(email_sender, manager):
    email_list = manager.get_email_list()
    if not email_list:
        print("Email list is empty. Cannot send emails.")
    else:
        for entry in email_list:
            email = entry["Email address"]
            name = entry["Prospect / Customer Name"]
            email_sender.send_email(email, name)
    input("\nPress Enter to return to the main menu.")
    
def emails_log(campaign_manager):
    campaign_manager.view_campaigns()
    input("\nPress Enter to return to the main menu.")


while True:
    choice = main_menu()
    clear_screen()

    if choice == '1':
        view_email_list(email_list_manager)
    elif choice == '2':
        add_new_email(email_list_manager)
    elif choice == '3':
        import_email_list(email_list_manager)
    elif choice == '4':
        create_email_campaign(campaign_manager)
    elif choice == '5':
        schedule_campaign(campaign_manager, email_list_manager, email_sender)
    elif choice == '6':
        emails_log(campaign_manager)
    elif choice == '7':
        print("Exiting EmailFlow. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the main menu.")
    clear_screen()
