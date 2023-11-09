import pandas as pd
import os
import sys

# Define column names in camelCase
userColumns = [
    "nameOfPerson",
    "ticketNumber",
    "eventName",
    "username",
    "password",
    "accountType",
    "transactionNumber",
    "creditOnFile"
]
ticketColumns = ["ticketNumber", 
                 "price", 
                 "eventName"]

eventColumns = ["eventName", 
                "remainingTickets",
                "date"]

transactionLogColumns = [
    "accountType",
    "username",
    "eventName"
    "ticketNumber"
]

# Path to the backend data directory
dataDirPath = "backendData"

# Ensure that the data directory exists
os.makedirs(dataDirPath, exist_ok=True)

# Function to load DataFrame from a text file or create a new one if the file does not exist
def loadOrInitializeDf(fileName, columns, sep='\t'):
    filePath = os.path.join(dataDirPath, fileName)
    if os.path.exists(filePath):
        df = pd.read_csv(filePath, sep=sep, dtype={'eventName': str})  # Ensure eventName is read as string

        # Safely convert 'remainingTickets' to int, replacing non-numeric values with NaN
        if 'remainingTickets' in df.columns:
            df['remainingTickets'] = pd.to_numeric(df['remainingTickets'], errors='coerce')
            df['remainingTickets'].fillna(0, inplace=True)  # Replace NaN with 0
            df['remainingTickets'] = df['remainingTickets'].astype(int)

        return df
    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(filePath, sep=sep, index=False)
        return df




# File names
userFileName = "users.txt"
ticketFileName = "tickets.txt"
eventFileName = "events.txt"
transactionLogFileName = "transactionLogs.txt"

# Load or create DataFrames
users = loadOrInitializeDf(userFileName, userColumns)
tickets = loadOrInitializeDf(ticketFileName, ticketColumns)
events = loadOrInitializeDf(eventFileName, eventColumns)
transactionLogs = loadOrInitializeDf(transactionLogFileName, transactionLogColumns)

# Login function
def login(username, password):
    global users
    if (username.lower() == 'admin' and password.lower() == 'admin'):
        return "admin"
    elif (username.lower() == 'agent' and password.lower() == 'agent'):
        return "agent"
    elif not users[(users['username'] == username) & (users['password'] == password)].empty:
        return "agent"
    else:
        return ""

# Add credit to the user's account
def addCredit(username, amount):
    global users

    user_index = users.index[users['username'] == username]
    if user_index.empty:
        print("User not found.")
        return

    try:
        user_row = users.loc[user_index]
        users.at[user_index[0], 'creditOnFile'] += amount
        
        recordTransaction(user_row["accountType"].values[0], username, "Credit Added", amount)
        print(f"${amount} credit added successfully to {username}'s account.")

    except ValueError:
        print("Invalid input. Please enter a numerical value.")

def createNewAccount():
    global users

    username = input("Enter new username or type 'EXIT' to cancel: ").strip()
    if username.lower() == 'exit':
        return

    if not users[users['username'] == username].empty:
        print("This username already exists. Please choose a different one.")
        createNewAccount()  # Recursive call
        return

    nameOfPerson = input("Enter your name: ")
    password = input("Enter your password: ")
    accountType = "agent"
    transactionNumber = 0
    creditOnFile = 0

    # Create a new user DataFrame
    new_user = pd.DataFrame({
        "nameOfPerson": [nameOfPerson],
        "ticketNumber": [0],
        "eventName": [""],
        "username": [username],
        "password": [password],
        "accountType": [accountType],
        "transactionNumber": [transactionNumber],
        "creditOnFile": [creditOnFile]
    })

    # Concatenate the new user DataFrame with the users DataFrame
    users = pd.concat([users, new_user], ignore_index=True)
    
    # Append to the transactionLogs DataFrame
    recordTransaction(accountType, username, f"New Account Created for {username}", 0)


    print(f"User {username} created successfully.")

# Create a new event
def createEvent(currentUsername, eventName, date, remainingTickets):
    global users, transactionLogs, events


    if len(eventName) > 15:
        print("Event name should be 15 characters or less. Returning to the main menu.")
        return False
    elif eventName.lower() == "creditAdded" or eventName.lower() == "nan":
        print("Event name cannot be 'creditAdded' or 'nan'. Returning to the main menu.")
        return False

    try:
        remainingTickets = int(remainingTickets)
        if remainingTickets <= 0 and remainingTickets > 9999:
            print("Invalid ticket count. Please enter a positive number. Returning to the main menu.")
            return False
    except ValueError:
        print("Invalid input for ticket count. Please enter a numerical value. Returning to the main menu.")
        return False


    newEvent = pd.DataFrame({
        "eventName": [eventName],
        "remainingTickets": [remainingTickets],
        "date": [date]
    })

    events = pd.concat([events, newEvent], ignore_index=True)

    # Record the transaction
    recordTransaction("admin", currentUsername, f"Event '{eventName}' Created", remainingTickets)

    print(f"Event '{eventName}' created successfully. Press Enter to continue...")
    return True


def addTicketsToEvent(eventName, username, num_tickets):
    global events

    # Find the event with the given name
    event_row = events[events['eventName'] == eventName]
    if event_row.empty:
        print(f"Event '{eventName}' not found.")
        return

    try:
        num_tickets = int(num_tickets)
        if num_tickets <= 0:
            print("Invalid number of tickets. Please enter a positive number.")
            return
    except ValueError:
        print("Invalid input for the number of tickets. Please enter a numerical value.")
        return

    # Increase the number of remaining tickets for the event
    events.loc[events['eventName'] == eventName, 'remainingTickets'] += num_tickets

    # Record the transaction
    recordTransaction("admin", username, f"Added {num_tickets} tickets to '{eventName}'", num_tickets)

    print(f"{num_tickets} tickets added successfully to '{eventName}'.")



def deleteTickets(username, eventName):
    global events

    # Find the event with the given name
    event_row = events[events['eventName'] == eventName]
    if event_row.empty:
        print(f"Event '{eventName}' not found.")
        return

    # Record the transaction before deleting
    recordTransaction("admin", username, f"Deleted event '{eventName}' ", event_row['remainingTickets'].values[0])

    # Delete the entire event
    events = events[events['eventName'] != eventName]

    print(f"Event '{eventName}' has been deleted.")




def recordTransaction(accountType, username, eventName, creditOnFile):
    global transactionLogs

    transaction_log = pd.DataFrame({
        "accountType": [accountType],
        "username": [username],
        "eventName": [eventName],
        "creditOnFile": [creditOnFile]
    }, index=[0])

    transactionLogs = pd.concat([transactionLogs, transaction_log], ignore_index=True)



def sellTicket(username, eventName, numTickets):
    global events, users, tickets
    
    # Convert eventName to string for consistent comparison
    eventName = str(eventName).strip()

    # Check if the event exists
    event_row = events[events['eventName'] == eventName]
    if event_row.empty:
        print(f"Event '{eventName}' not found.")
        return

    # Check if there are enough remaining tickets
    remaining_tickets = int(event_row['remainingTickets'].iloc[0])
    if numTickets > remaining_tickets:
        print(f"Not enough tickets available for '{eventName}'. Only {remaining_tickets} remaining.")
        return

    # Update the remaining tickets for the event
    events.loc[events['eventName'] == eventName, 'remainingTickets'] -= numTickets

    # Generate ticket numbers and add them to the tickets DataFrame
    max_ticket_number = tickets['ticketNumber'].max() if not tickets.empty else 0
    new_ticket_numbers = range(max_ticket_number + 1, max_ticket_number + numTickets + 1)
    new_tickets = pd.DataFrame({
        'ticketNumber': new_ticket_numbers,
        'price': [0] * numTickets,  # Assuming a price of 0 for simplicity
        'eventName': [eventName] * numTickets,
        'username': [username] * numTickets  # Assign the tickets to the buyer's username
    })
    tickets = pd.concat([tickets, new_tickets], ignore_index=True)

    print(f"Successfully sold {numTickets} tickets for '{eventName}'.")


    
def returnTicket(username, eventName, numTickets):
    global events, users, tickets

    # Check if the event exists
    event_row = events[events['eventName'] == eventName]
    if event_row.empty:
        print(f"Event '{eventName}' not found.")
        return

    # Convert numTickets to int
    try:
        numTickets = int(numTickets)
        if numTickets <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number of tickets. Please enter a positive integer.")
        return

    # Check if the user has that many tickets for the event
    user_tickets = tickets[(tickets['username'] == username) & (tickets['eventName'] == eventName)]
    if user_tickets.shape[0] < numTickets:
        print(f"User '{username}' does not have {numTickets} tickets for event '{eventName}'.")
        return

    # Return the tickets
    # Remove the sold tickets from the tickets DataFrame
    tickets_to_return = user_tickets.head(numTickets)
    tickets = tickets.drop(tickets_to_return.index)

    # Update the remaining tickets for the event
    events.loc[events['eventName'] == eventName, 'remainingTickets'] += numTickets

    print(f"Successfully returned {numTickets} tickets for '{eventName}'.")

    # Record the transaction
    recordTransaction("agent", username, f"Returned {numTickets} tickets for '{eventName}'", numTickets)





# Exit the program and save DataFrames
def exitProgram():
    global users, tickets, events, transactionLogs

    users.to_csv(os.path.join(dataDirPath, userFileName), sep='\t', index=False)
    tickets.to_csv(os.path.join(dataDirPath, ticketFileName), sep='\t', index=False)
    events.to_csv(os.path.join(dataDirPath, eventFileName), sep='\t', index=False)
    transactionLogs.to_csv(os.path.join(dataDirPath, transactionLogFileName), sep='\t', index=False)
    print("Databases saved successfully.\n\n*****TERMINATING THE PROGRAM SUCCESSFULLY*****")
    sys.exit()
