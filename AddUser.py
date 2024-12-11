#This is the add user file, it will basically check user inputs making sure they are formatted correctly then they will write to the json file
#This file is caled whenever the user wants to create 

#imports
import re 
import json
import os
import random
from database import session, Student #THIS IS IMPORTANT FOR DATABASE

#Generation of the very next ID when needed 
def generate_next_id(students):
    #700000 is base ID
    base_id = 700000
    
    #Setting up exsisting ids
    existing_ids = {int(student['id']) for student in students} #id in the student.json
    
    # adding 1 to current id to give the next person created +1 (A good example is 700000 going to 700001)
    while base_id in existing_ids:
        base_id += 1
        
    #Just in case we go over, will never happen though
    if base_id > 700999:
        raise ValueError("No more IDs available in the 700xxx range")
        
    return str(base_id)

#start of the main function
def add_user():
    #This is to make the rules more stylish 
    #Used colorama more than the class I made: color_Text
    class color_Text:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    #This is all a cool rule box the user will get when making a student
    print(color_Text.BOLD + "==========================Add Student========================\n" + color_Text.END)
    print(color_Text.BOLD + "                          RULES" + color_Text.END)
    print(color_Text.UNDERLINE + "1. The first letter of first and last name must be capitalized")
    print("2. First and last name must each have at least two letters")
    print("3. No digit allowed in the first or last name")
    print("4. Student ID is 6 digits long and MUST start with 700 (700xxx)")
    print("5. Phone number must be in the (xxx-xxx-xxxx) format")
    print("6. Student major must be in CS, CYBR, SE, IT, or DS")
    print("7. Graduation year must be within 2024 - 2099\n\n" + color_Text.END)


    #This will load the json file with the correct file path. Make sure you arent creating extra folders or else it will make student.json in wrong folder!
    file_path = 'ProjectJSONs/student.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Handle both cases, when data is a list and when it's a dict
            if isinstance(data, list):
                students = data
                #This should convert it to a new format
                data = {'students': students}
            else:
                students = data.get('students', [])
    except (FileNotFoundError, json.JSONDecodeError): #exception
        students = []
        data = {'students': students}

    #WHile loop to Start of making the student names 
    while True:
        student_name = input("Enter Student Name (First & Last): ").strip() #gets rid of whitespace
        name_parts = student_name.split() #will split name in 2 checking that is there is only 2

        if len(name_parts) == 2: #length making sure it is two characters at least, since some people how two letters in their name
            first_name, last_name = name_parts #2 parts
            if (
                first_name.isalpha() and last_name.isalpha()
                and first_name[0].isupper() and last_name[0].isupper()#caps
                and len(first_name) >= 2 and len(last_name) >= 2#this is checking to make sure the length of the names are at least 2 characters long
            ):
                print("✅Name is valid.\n")
                break
            else:
                print("❌Invalid name. Ensure both names have at least 2 letters, start with a capital letter, and contain no digits.\n")
        else:
            print("❌Invalid name. Please enter both first and last names separated by a space.\n")

    # Generates id for person that is being currently created
    try:
        student_id = generate_next_id(students)
        print(f"Assigned Student ID: {student_id}")
    except ValueError as e:
        print(f"Error: {e}")
        return False
    
    # Validate stdent age
    while True:
        try:
            student_age = input("Enter the age of student: ").strip() # User prompt
            age = int(student_age)
            if 17 <= age <= 99: # Realistic age, but 99 is pushin it 
                print("Age is valid")
                break
            else:
                print("❌ Please enter in a realistic age!\n")
        except ValueError:
            print("❌ Invalid input. Please enter a numeric age\n")

    # Validate student gender for student creation
    while True:
        student_gender = input("Enter student gender Male, Female or Other (M,F,O): ").strip().upper()
        if student_gender in ['M', 'F', 'O', 'MALE', 'FEMALE', 'OTHER']: #This is for if anyone actually types out the whole gender
            print("✅ Gender is valid")
            break
        else:
            print("❌ Invalid gender. Please enter M, F or O")

    # Validate student phone number!
    while True:
        student_phone_number = input("Enter phone number (xxx-xxx-xxxx): ").strip() #strip method agaim
        # Check for duplicate phone number
        if any(existing_student.get('phone', '') == student_phone_number for existing_student in students): #this will check that no 2 students can have the same phone #
            print("⚠️Error: This Phone Number already exists in the system.")
            continue

        if re.match(r'^\d{3}-\d{3}-\d{4}$', student_phone_number): #using the match method to make sure that the correct number of digits is provided
            print("✅ Student Phone Number is valid\n")
            break
        else:
            print("❌Invalid Student Phone Number. Please use the format xxx-xxx-xxxx\n")

    # Creating student major
    valid_majors = {'CS', 'CYBR', 'SE', 'IT', 'DS'}
    while True:
        student_major = input("Enter student major (CS, CYBR, SE, IT, DS): ").strip().upper() #will strip whitespace and make the letters uppercase no matter user input
        if student_major in valid_majors:
            print("✅ Student Major is valid\n")
            break
        else:
            print("❌Invalid Student Major. Please choose from: CS, CYBR, SE, IT, or DS\n")


    #Collects a users estimated graduation date
    def GradYearChecker():
        while True:
            grad_year = input("Enter estimated graduation year in the format: (20xx): ").strip()
            try:
                grad_year = int(grad_year) #Simple comparison for grad year date
                if 2024 <= grad_year <= 2099:
                    print("✅ Students Estimated Grad Year is valid")
                    return str(grad_year)  # Return as string for JSON consistency
                else:
                    print("That is impossible. Please enter a realistic year!\n")
            except ValueError:
                print("❌Invalid input. Please enter a valid year.\n")

    # Before creating student_info, call the function
    grad_year = GradYearChecker()
        
    # We added the classes dict for the classes
    major_classes = {
        'CS': ['CS1000', 'CS2300', 'CS2400', 'CS1030'],
        'CYBR': ['CS2300', 'CYBR1000', 'CYBER2500', 'CS2010'],
        'SE': ['SE1000', 'CS1030', 'CYBR2500', 'SE2050'],
        'IT': ['CS2400', 'IT1000', 'CS1030', 'CYBR1000'],
        'DS': ['ASCT2030', 'DSA1080', 'CS1030', 'CS2300']
    }

    #Generates a random GPA with the random module
    import random
    student_gpa = round(random.uniform(0.1, 4.0), 2)
    print(f"\n✅ Student's initial GPA has been randomly generated and set to: {student_gpa} if you wish to change it please check out the Modify Student Option in main menu.\n")

    # Student Info Dict
    student_info = {
        "name": student_name,
        "id": student_id,
        "age": age,  
        "gender": student_gender,
        "phone": student_phone_number,
        "major": student_major,
        "classes": major_classes[student_major], # We added classes to be sent to the json based on selected major
        "grad_year": grad_year, # We also added a estimated graduation year to the student info
        "gpa": student_gpa #Added the GPA
    }

    #Add new student to the students list
    students.append(student_info) #using append method
    data['students'] = students

    # this will write back to the json!!!
    #lots of exceptions just in case stuff goes wrong...
    try:
        # Write to JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            
        # Write to database
        student_db = Student(
            id=student_info['id'],
            name=student_info['name'],
            age=student_info['age'],
            gender=student_info['gender'],
            major=student_info['major'],
            phone=student_info['phone'],
            gpa=student_info['gpa']
        )
        session.merge(student_db)  #Merge function op, writes to it if it exsists
        session.commit()
        
        print("\n✅Success! Student information has been SAVED!")
        return True
    except PermissionError:
        session.rollback()
        print("⚠️\nError: Permission denied. Unable to write to the file.")
        return False
    except IOError as e:
        session.rollback()
        print(f"⚠️\nError saving student information: {str(e)}")
        return False
    except Exception as e:
        session.rollback()
        print(f"⚠️\nUnexpected error occurred: {str(e)}")
        return False