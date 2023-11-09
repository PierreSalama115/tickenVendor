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
                 "remainingTickets"]
eventColumns = ["eventName", 
                "remainingTickets"]

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


#FOR NOW THE ONLY THING THAT WORKS IS agent and admin login, next iteration will take into account
#the created users and also allow them to login since they've created account

def login(username, password):
    #WE HAVE TO DECLARE IT GLOBALLY IN THIS LOCAL SCOPE SO WE CAN ACCESS IT
    global users
    # Check if username and password are in predefined list
    if username.lower() in ['agent', 'admin'] and password.lower() in ['agent', 'admin']:
        return True
    # Check if username and password are in the users DataFrame
    elif users[(users['username'] == username) & (users['password'] == password)].shape[0] > 0:
        return True
    else:
        return False

def addCredit(username, amount):
    global users

    # Ensure the user exists
    user_row = users[users['username'] == username]
    if user_row.empty:
        print("User not found.")
        return

    try:
        # Create a new DataFrame for the transaction log
        transaction_log = pd.DataFrame({
            "nameOfPerson": user_row["nameOfPerson"].values[0],
            "ticketNumber": 0,
            "eventName": "Credit Added",
            "username": username,
            "password": user_row["password"].values[0],
            "accountType": user_row["accountType"].values[0],
            "transactionNumber": user_row["transactionNumber"].values[0] + 1,
            "creditOnFile": user_row["creditOnFile"].values[0] + amount,
        }, index=[0])

        # Concatenate the transaction log DataFrame with the users DataFrame
        users = pd.concat([users, transaction_log], ignore_index=True)

        print(f"${amount} credit added successfully to {username}'s account.")

    except ValueError:
        print("Invalid input. Please enter a numerical value.")


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

    # Create a new DataFrame for the new user
    new_user = pd.DataFrame({
        "nameOfPerson": nameOfPerson,
        "ticketNumber": 0,
        "eventName": "",
        "username": username,
        "password": password,
        "accountType": accountType,
        "transactionNumber": transactionNumber,
        "creditOnFile": creditOnFile
    }, index=[0])

    # Concatenate the new user DataFrame with the users DataFrame
    users = pd.concat([users, new_user], ignore_index=True)

    print(f"User {username} created successfully.")

def exitProgram():

    global users, tickets, events

    # Save the current state of DataFrames to text files
    users.to_csv(os.path.join(dataDirPath, userFileName), sep='\t', index=False)
    tickets.to_csv(os.path.join(dataDirPath, ticketFileName), sep='\t', index=False)
    events.to_csv(os.path.join(dataDirPath, eventFileName), sep='\t', index=False)
    print("Databases saved successfully.\n\n*****TERMINATING THE PROGRAM SUCCESFULLY*****")
    sys.exit()
