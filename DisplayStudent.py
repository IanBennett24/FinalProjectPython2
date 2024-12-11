'''
This is the display students class file that will display all the students, additionally we wanted to add the ability to search for students based on a given graduation 
date or their major
'''
#All our imports!
import json 
#Creating a class
class DisplayStudent:
    # This is the constructor that will load the students.json file
    def __init__(self, json_file):
        self.json_file = json_file
        self.students = self.load_students()
 
        self.check_mark = "\u2705"
        self.envelope = "\u2709"  
        self.cross_mark = "\u274C"  
        self.telephone = "\u260E"
        
    # This is the display student class that will display what is in the .json file
    # Displays all our json fields, except the admin.json. 
    def display_student(self, student):
        if student:
            print("\n" + "=" * 30)
            print(f"Student Information:")
            print(f"ID:    {student['id']}")
            print(f"Name:  {student['name']}")
            print(f"Phone: {student['phone']}")
            print(f"Major: {student['major']}")
            print(f"Grad Year: {student['grad_year']}") 
            print(f"GPA: {student['gpa']}")
            print(f"Classes:") # Added classes 
            for i, class_name in enumerate(student.get('classes', []), 1):
                print(f"  {i}. {class_name}")
            print("=" * 30)
        else:
            print("\n ⚠️Error: No student information to display.")#gives user an error message


    #method that displays all of the students
    def display_all_students(self):
        self.display_filtered_students()

    # Method that will search the .json file for students in that major or all of them
    def display_filtered_students(self, major=None):
        filtered_students = self.students
        #Filters out students that dont match the major
        if major:
            filtered_students = [student for student in self.students if student['major'].upper() == major.upper()]
        # If no students match the major the user will be notified
        if not filtered_students:
            print(f"\n ⚠️No students found" + (f" with major {major}." if major else "." ))#Error message
            return
        # Prints the student information
        for student in filtered_students:
            print(f"\nDisplaying information for student ID: {student['id']}")
            self.display_student(student)

    # This method will filter the students by their major
    def filter_by_major(self):
        #Gives the user a list of possible majors to choose from 
        print("\nAvailable majors:")
        majors = set(student['major'] for student in self.students)
        for major in majors:
            print(f"* {major}")
        
        #Asks the user to enter a major or press enter to see all of the students
        while True:
            major = input("\nEnter the major to filter by (or press Enter to see all students): ").strip().upper()
            # If its not a major then all of the students are displayed otherwise the 
            # Method that gets students in a given major is called
            if not major:
                self.display_all_students()
                break
            elif major in majors:
                self.display_filtered_students(major)
                break
            else:
                print("❌ Invalid major. Please try again.")

    # Method that reads the .json file and converts the data to be printed to the user
    def load_students(self):
        try:
            with open('ProjectJSONs/student.json', 'r') as f: #JSON File containing the student json
                data = json.load(f)
                return data.get('students', [])
        except FileNotFoundError:
            print(f"\n ⚠️Error: File   '{self.json_file}' not found.")
            return []
