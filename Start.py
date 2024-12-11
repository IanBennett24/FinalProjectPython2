'''
This is the start file that will serve as main for our project this file will get the users input for what they would like to do
they will then be routed to one of the classes for that task. When they are done the will return to the menu where they can select
another task or exit
'''
#our imports
import json
import re

# Imports Classes from their files
from ModifyStudent import ModifyStudent
from QueryStudent import QueryStudent
from AddUser import *
from DeleteUser import *
from ShowStudent import ShowStudent

class color_Text: #was used throughout program as cool text edits
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Method to get user input 
def get_input(prompt, default=None):
    user_input = input(prompt)
    return user_input if user_input else default

# Method to get the users choice for where they want to be routed
def get_choice():
    while True:
        try:
            choice = int(input("Please Enter The Operation Code (1 - 6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

# The main method that will contain the menu, prompt the user, get the users input and route them
def main():
    # Try to get the current admin ID from the admin.json file
    try:
        with open('ProjectJSONs/admin.json', 'r') as file:
            admin_data = json.load(file)
            # Ensure compatibility with different file formats
            admin_list = admin_data.get('admin', admin_data)
            #get the last admin in the list (most recently created)
            current_admin_id = admin_list[-1]['id'] if admin_list else 'N/A'
    except (FileNotFoundError, IndexError, json.JSONDecodeError):
        current_admin_id = 'N/A'

    while True:
        print("=" * 60)
        print("     ✏️   Student Management System v1.2")
        print(color_Text.BOLD + f"           Welcome ADMIN: {current_admin_id}" + color_Text.END)#will showcase the most recently logged in admin
        print()
        print("   ➡️     1. Add Student")
        print("   ➡️     2. Preview Students")
        print("   ➡️     3. Modify Student")
        print("   ➡️     4. Delete Student")
        print("   ➡️     5. Query Student")
        print("   ➡️     6. Log Out" )
        print("=" * 60)
        
        choice = get_choice()

        # If they choose 1 they will be able to add a user
        if choice == 1:
            add_user()

        # If they choose 2 they will be able to show users
        elif choice == 2:
            ShowStudent('ProjectJSONs/student.json').search_by_menu()

        # If they choose 3 they will be able to modify a user
        elif choice == 3:
            ModifyStudent('ProjectJSONs/student.json').modify_student()

        # If they choose 4 they will be able to delete students
        elif choice == 4:
            delete_user()

         # If they choose 5 they will be able search up a students grades
        elif choice == 5:
            QueryStudent('ProjectJSONs/student.json').query_student()

        # If they choose 6 the program will terminate
        elif choice == 6:
            confirm = input("\nAre you sure you want to exit? (Y/N): \n").upper()
            if confirm in ['Y', 'YES']:
                print("Exiting System, Logging Out!\n")
                break

        

