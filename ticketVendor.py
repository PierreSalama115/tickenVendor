import os
from datetime import datetime, timedelta
import ticketVendorBackEnd
import sys


class User:
    """
    In the User class the program takes in the the strings username,
    password and checks if the user that logged in is an admin
    """

    def __init__(self, username: str, password: str, is_admin: bool = False):
        """
        (User, str, str, bool) -> None
        this does somerjj
        """
        self.username = username
        self.password = password
        self.is_admin = is_admin


class System:
    """
    This class stores the users logged in an array called users cand checks the current user.
    there are methods in this class which gives the user options to what the want to do to contine with the program.
    For example when the user enters the option L the System will output the corresponding output the the option L.

    """

    # This method has an array to store the users logged in and the current_user is None and is_logged_in is false because  no one is logged in yet
    def __init__(self):
        self.users = []
        self.current_user = None
        self.is_logged_in = (
            False  # New variable to track login state. This variable is a boolean
        )

    # Adding User to the users array
    def addUser(self, user):
        self.users.append(user)

    # This is the login method where the user will enter their username and password to log in

    def optionL(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        if ticketVendorBackEnd.login(username, password):
            # Login successful
            self.current_user = username
            self.is_logged_in = True
            print(f"****Currently logged in as {username} ****")
        else:
            # Login failed
            print("Invalid credentials. Please try again.")

    # In the method optionL it logs in the user
    

    # In the method optionN it allows  the user to create a new account
    def optionN(self):
        ticketVendorBackEnd.createNewAccount()

    def option1(self):
        if self.is_logged_in:  # Check the login state variable
            print("You chose to Add Credit.")
            amount = input("Enter the credit amount (not over 1000$):  \n")
            if amount.isdigit() and int(amount) <= 1000:
                credit_card = input("Enter your credit card number (16digits-MM/YY-CVV):  \n")
                if len(credit_card) == 23:
                    # Call the backend function to add credit
                    ticketVendorBackEnd.addCredit(self.current_user, int(amount))  # Pass the current username
                    print("You have successfully added credit to your account. Press Enter to continue...")
                else:
                    print("Credit Card number should be (16digits-MM/YY-CVV). Returning to the main menu...")
            else:
                print("Invalid credit amount. Returning to the main menu.")
        else:
            print("You need to be logged in to access this option.")
        input("Press Enter to continue...  \n")
    


    # In the method option2 it allows the user to create an event from tomorrow's date to 2 years from today if the user is an admin
    def option2(self):
        if self.is_logged_in:  # Check the login state variable
            if self.current_user.is_admin:  # Check if the user is an admin
                print("You selected 'Create Event'.")
                event_name = input("Enter the event name (15 characters at most):  \n")
                if len(event_name) <= 15:
                    event_date = input(
                        "Enter the event date (YYYYMMDD) from tomorrow to two years from today: \n "
                    )
                    if len(event_date) == 8 and event_date.isdigit():
                        current_date = datetime.now()
                        tomorrow = current_date + timedelta(days=1)
                        two_years_from_today = current_date + timedelta(days=730)

                        event_date_obj = datetime.strptime(event_date, "%Y%m%d")

                        if tomorrow <= event_date_obj <= two_years_from_today:
                            tickets = input(
                                "Enter the number of tickets to allocate for the event (at most 9999):  \n"
                            )
                            if tickets.isdigit() and 0 < int(tickets) <= 9999:
                                print("Press Enter to continue...")
                            else:
                                print(
                                    "Invalid ticket number. Should be a positive integer at most 9999. Returning to the main menu."
                                )
                        else:
                            print(
                                "Event date should be from tomorrow to two years from today. Returning to the main menu."
                            )
                    else:
                        print(
                            "Invalid date format. Event date should be in YYYYMMDD format. Returning to the main menu."
                        )
                else:
                    input("Successful...Press Enter to continue...  \n")
            else:
                print("You need to be an admin to create an event")
                input("Press Enter to continue... \n")
        else:
            print("You need to be logged in to access this option.")
            input("Press Enter to continue... \n")

    # The method option3 is to add tickets to an existing event and the user needs to be an admin to access this option
    def option3(self):
        if self.is_logged_in:
            if self.current_user.is_admin:  # Check the login state variable
                event_name = input("Enter the event name:  \n")
                tickets = input("Enter the number of tickets:  \n")
                # Implement logic for adding tickets to an existing event
                print("Press Enter to continue...")
            else:
                print("You need to be an admin to access this option.")

    # The method option4 is to cancel tickets and delete any existing events, and the user needs to be an admin to access this option
    def option4(self):
        if (
            self.is_logged_in and self.current_user.is_admin
        ):  # Check the login state variable
            if self.current_user.is_admin:
                event_name = input("Enter the event name:  \n")
                # Implement logic for canceling tickets and deleting an event
                print("Press Enter to continue...")
            else:
                print("You need to be an admin to access this option.")

    # This method option5 is to sell a number of tickets for an event and enter the event name and the number of tickets
    def option5(self):
        if self.is_logged_in:  # Check the login state variable
            event_name = input("Enter the event name:  \n")
            ticket_number = input("Enter a ticket number:  \n")
            # Implement logic for selling tickets for an existing event
            print("Press Enter to continue...")

    # The method option6 is to return tickets for any existing events, and the user needs to be an admin to access this option
    def option6(self):
        if self.is_logged_in:  # Check the login state variable
            if self.current_user.is_admin:
                event_name = input("Enter the event name: \n ")
                ticket_number = input("Enter a ticket number: \n ")
                # Implement logic for returning tickets of an existing event
                print("You returned the ticket. Press Enter to continue.")
            else:
                print("You need to be an admin to access this option.")

    # The method option7 is to log out of the system
    def option7(self):
        self.current_user = None
        self.is_logged_in = False  # Set login state to False
        print("Logged out successfully. Press Enter to continue.")

    #The method option8 is to exit the program,this was an orginal requirment
    def optionQ(self):
        ticketVendorBackEnd.exitProgram()  # Save databases and reset state
        self.current_user = None
        self.is_logged_in = False
        print("saving to database...\n" + "***TERMINATE PROGRAM****")
        ticketVendorBackEnd.exitProgram()
        
    # This is the main menu that will be displayed when the program is run and the user picks there choice
    def main_menu(self):
        while True:
            print("L. Login")
            print("N. Create New Account")
            print("1. Add Credit")
            print("2. Create Event")
            print("3. Add")
            print("4. Delete")
            print("5. Sell")
            print("6. Return")
            print("7. Logout")
            print("Q. Exit")
            choice = input("Enter your choice: \n")

            # The options will be matched to its corresponding method
            action_mapper = {
                "L": self.optionL,
                "N": self.optionN,
                "1": self.option1,
                "2": self.option2,
                "3": self.option3,
                "4": self.option4,
                "5": self.option5,
                "6": self.option6,
                "7": self.option7,
                "Q": self.optionQ,
            }

            action = action_mapper.get(choice.upper(), None)

            if action:
                if (
                    choice.upper() in ["1", "2", "3", "4", "5", "6", "7"]
                    and not self.is_logged_in
                ):
                    print("You need to be logged in to access this option.")
                else:
                    action()
            else:
                print("Invalid choice. Please enter a valid option.")


# This is the main where we pass in the parameter values for the User class
if __name__ == "__main__":
    system = System()
    system.addUser(User("admin", "admin", is_admin=True))
    system.addUser(User("agent", "pass", is_admin=False))

    system.main_menu()
