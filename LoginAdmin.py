#This is the file where to start the program now, it will bring you to the Admin login page
#Make sure you guys have colorama downlaoded so it will showcase the fancy colors
# I used python3 -m pip install colorama in cmd to donwload it

# All of our imports
import json
import re 
import os
import hashlib

from Start import *
from database import session, AdminInfo

# This is to make the rules more stylish, however not used as much as wished
class color_Text:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# A while loop to see what the user chooses at the login page. 
def get_log_choice():
    while True:
        try:
            choice = int(input("Please Enter The Operation Code (1 - 3): "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 3!")#Prints if user doesnt select correct choice
        except ValueError:
            print("\nInvalid input. Please enter a number (1-3)")#Exception if for whatever reason something doesnt work

# Function should hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()#hasing it to the sha256

#Function to check to make sure user followed rules when making username
def validate_username(username):
    # Username must start with a capital letter and be 3-6 characters long
    if not re.match(r'^[A-Z][a-zA-Z]{2,5}$', username):
        return False
    return True

# Function to validate password, literally samething as validate_username, just for password and different match case
def validate_password(password):
    #Trying to keep passwords requirments
    if not re.match(r'^[!@#$%^&*][A-Za-z0-9]{5,11}$', password):
        return False
    
    #Just some addiontal checks
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    
    return True

# login start function start
def login_start():
    file_path = 'ProjectJSONs/admin.json' #Writes to the json in this file directory 
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Open or create the file
        with open(file_path, 'a+') as file:
            file.seek(0)
            try:
                data = json.load(file)
                # Handle both cases, when data is a list and when it's a dict
                if isinstance(data, list):
                    admin = data
                    # This should convert it to a new format
                    data = {'admin': admin}
                else:
                    admin = data.get('admin', [])
            except (json.JSONDecodeError, EOFError): #exceptions
                admin = []
                data = {'admin': admin}

    except FileNotFoundError: #another exception
        admin = []
        data = {'admin': admin}

    while True: #While true loop for the main menu of the login admin page
        print("=" * 60)
        print("        Student Management System:" + color_Text.BOLD, " ADMIN LOGIN" + color_Text.END)  #Admin looks cool bright and red
        print("        1. Login")
        print("        2. Register Admin")
        print("        3. Exit")
        print("=" * 60)

        choice = get_log_choice()
        #BEgin the login process
        if choice == 1:
            user_choice = input("Enter Admin Username: ").strip()#strips whitespace
            pass_choice = input("Enter Admin Password: ").strip()
            admin_loging_process(user_choice, pass_choice, file_path)

        #Register the admin with a prompt to confirm
        elif choice == 2:
            confirmAdminMake = input("Do you want to create a new admin? (Y/N): ").upper()#upper ensures that the input gets turned to caps
            if confirmAdminMake in ['Y', 'YES']:
                print()
                add_admin(file_path)
            else:
                #This will return to the login menu if anything other than Y/YES is entered
                continue
                    #Do the exiting process
        elif choice == 3:
            confirm = input("Are you sure you want to exit the system? (Y/N): ").upper()#upper ensures that the input gets turned to caps, same as earlier
            if confirm == 'Y' or confirm == 'YES': #this does the same as confirmadminmake but wanted to try something different
                quit()
                break
            else:
                continue
        

        input("\nPress Enter to continue...")#spaces out program nicely 

def admin_loging_process(username, password, file_path): #The hardest function in the file, needs to takes the username and password and checks if it exists within admin.json
    try:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                admin_list = data.get('admin', []) if isinstance(data, dict) else data #checking the 'admin' portion of the json

                # Checking if there are no admin accounts
                if not admin_list:
                    print("⚠️ No admin accounts exist. Please register an admin first.") #big error sign good for user input
                    return

                # Check if the provided username and hashed password match an admin
                for admin in admin_list:
                    if admin['id'] == username and admin['password'] == hash_password(password):
                        print("✅ Login successful!")
                        from Start import main  # Import here to avoid circular import
                        main()  #calling the main function from Start.py here
                        return
                
                print("❌ Username or Password is wrong!")#wrong answer
            
            except json.JSONDecodeError:
                print("⚠️ Admin data file is empty or corrupted. Please register an admin first.")#exception, helpful for when testing out file sharing between group members
    
    except FileNotFoundError:
        print("⚠️ Admin data file not found. Please register an admin first.")# Another exception


# Start of the function for adding an admin
def add_admin(file_path):
    # This is all a cool rule box for logging in  
    print( "==========================Add Admin======================== ")
    print("                                   RULES" )
    print(color_Text.UNDERLINE +"1. Username must start with a capital letter")
    print("2. Username must be between 3 and 6 characters long")
    print("3. Password must start with one of the following special characters !@#$%^&*")
    print("4. Password must contain at least one digit, one lowercase letter, and one uppercase letter")
    print("5. Password is between 6 and 12 letters long\n\n"+ color_Text.END)

    while True:
        # Username validation
        while True:
            admin_user = input("\nEnter an admin username (Starting with a capital letter and being 3 - 6 characters long): ").strip()# Strip the whitespace 
            
            # Validate username format
            if not validate_username(admin_user):
                print("\n❌ Invalid Admin username. Must start with a CAPITAL LETTER and be 3-6 characters long.")
                continue
            
            # Load existing admins
            with open(file_path, 'r') as file:
                try:
                    existing_data = json.load(file)
                    existing_admins = existing_data.get('admin', []) if isinstance(existing_data, dict) else existing_data
                except (json.JSONDecodeError, EOFError):
                    existing_admins = []

            # Check for duplicate usernames
            if any(existing_admin.get('id', '') == admin_user for existing_admin in existing_admins): #Reads the Id part in the admin.json
                print("\n ⚠️ Error: This Admin username already exists in the system ⚠️")
                continue
            
            break

        # Password validation
        while True:
            admin_pass = input("\nEnter admin password: ")#user input
            
            if not validate_password(admin_pass):
                print("❌ Invalid password. Please follow the rules:")
                print("1. Must start with !@#$%^&*")
                print("2. Must contain at least one digit, one lowercase, and one uppercase letter")
                print("3. Length between 6 and 12 characters\n")
                continue
            
            # Confirm password
            confirm_pass = input("\nConfirm password: ")
            if admin_pass != confirm_pass:
                print("\n❌ Passwords do not match. Please try again.")# Prompts user with incorrect message
                continue
            
            break

        #Hashed pass
        hashed_pass = hash_password(admin_pass)

        # Prepare new admin entry in the admin,json. only 2 fields, id and password
        admin = {
            'id': admin_user,
            'password': hashed_pass
        }

        try:
            # Write to JSON
            with open(file_path, 'r+') as file:
                try:
                    existing_data = json.load(file)
                    
                    #Making sure data is in the correct format
                    if isinstance(existing_data, list):
                        existing_data = {'admin': existing_data}
                    
                    # Add new admin!
                    existing_data['admin'].append(admin) #append adding on 
                except (json.JSONDecodeError, EOFError):
                    # If file is empty or invalid, create new data
                    existing_data = {'admin': [admin]}

                # Reset file pointer and write updated data
                file.seek(0)
                file.truncate()
                json.dump(existing_data, file, indent=4)

            # Write to database
            admin_db = AdminInfo(
                name=admin_user,  # name is the field in AdminInfo class
                password=hashed_pass
            )
            session.merge(admin_db)  #merge will update if exists, insert if doesn't
            session.commit()

            print("✅ Admin successfully registered!")
            break
        except Exception as e:
            session.rollback()
            print(f"❌ Error registering admin: {str(e)}")

#CAlling back the main funct
login_start()
