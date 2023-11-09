import pandas as pd
import os

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

ticketColumns = ["ticketNumber", "price", "remainingTickets"]

eventColumns = ["eventName", "remainingTickets"]

# Path to the backend data directory
dataDirPath = "backendData"

# Ensure that the data directory exists
os.makedirs(dataDirPath, exist_ok=True)

# Function to load DataFrame from a text file or create a new one if file does not exist
def loadOrInitializeDf(fileName, columns, sep='\t'):
    filePath = os.path.join(dataDirPath, fileName)
    if os.path.exists(filePath):
        return pd.read_csv(filePath, sep=sep)
    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(filePath, sep=sep, index=False)
        return df

# File names
userFileName = "users.txt"
ticketFileName = "tickets.txt"
eventFileName = "events.txt"

# Load or create DataFrames
users = loadOrInitializeDf(userFileName, userColumns)
tickets = loadOrInitializeDf(ticketFileName, ticketColumns)
events = loadOrInitializeDf(eventFileName, eventColumns)

def login(username, password):
    if username.lower() in ['agent', 'admin'] and password.lower() in ['agent', 'admin']:
        # Login successful
        return True
    else:
        # Login failed
        return False

def createNewAccount():
    global users

    username = input("Enter new username or type 'EXIT' to cancel: ").strip()
    if username.lower() == 'exit':
        return

    if username.lower() in ['agent', 'admin']:
        print("This username is reserved. Please choose a different one.")
        createNewAccount()  # Recursive call
        return

    # Check if username already exists in users DataFrame
    if not users[users['username'] == username].empty:
        print("This username already exists. Please choose a different one.")
        createNewAccount()  # Recursive call
        return

    # Proceed with new account creation
    nameOfPerson = input("Enter your name: ")
    password = input("Enter your password: ")
    accountType = "agent"
    transactionNumber = 0
    creditOnFile = 0

    # Adding new user to DataFrame
    newUser = {
        "nameOfPerson": nameOfPerson,
        "ticketNumber": 0,
        "eventName": "",
        "username": username,
        "password": password,
        "accountType": accountType,
        "transactionNumber": transactionNumber,
        "creditOnFile": creditOnFile
    }

    users = users.append(newUser, ignore_index=True)
    
    print(f"User {username} created successfully.")

def defAddCredit(username):
    global users

    # Ensure the user exists
    if username not in users['username'].values:
        print("User not found.")
        return

    try:
        # Prompt for the credit amount
        amount = float(input("Enter the credit amount to add: $"))
        if amount <= 0:
            print("Invalid amount. Please enter a positive number.")
            return

        # Update the user's credit in the DataFrame
        users.loc[users['username'] == username, 'creditOnFile'] += amount

        print(f"${amount} credit added successfully to {username}'s account.")

        # Optionally, save the updated DataFrame to the file
        users.to_csv(os.path.join(dataDirPath, userFileName), sep='\t', index=False)
    except ValueError:
        print("Invalid input. Please enter a numerical value.")



def exitProgram():
    global users, tickets, events

    # Save the current state of DataFrames to text files
    users.to_csv(os.path.join(dataDirPath, userFileName), sep='\t', index=False)
    tickets.to_csv(os.path.join(dataDirPath, ticketFileName), sep='\t', index=False)
    events.to_csv(os.path.join(dataDirPath, eventFileName), sep='\t', index=False)
    print("Databases saved successfully.")
