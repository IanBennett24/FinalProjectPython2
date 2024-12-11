'''
This is the file to query a student
'''
import json
import re

class QueryStudent:
    # Constructor method
    def __init__(self, json_file):
        self.json_file = json_file
        self.students = self.load_students()
 
        # Stores unicode as instance attributes
        self.check_mark = "\u2705"
        self.envelope = "\u2709"  
        self.cross_mark = "\u274C"  
        self.telephone = "\u260E" 

    # Loads a student from the student.json file
    # if the file cant be found then an error is thrown
    def load_students(self):
        try:
            with open("ProjectJSONs/student.json", 'r') as f:
                data = json.load(f)
                return data.get('students', [])
        except FileNotFoundError:
            return []

    # Method to display students information if there is any otherwise the 
    # User will be notified
    def display_student(self, student):
        if student:
            print("\n" + "=" * 30)
            print(f"Student Information:")
            print(f"ID:    {student['id']}")
            print(f"Name:  {student['name']}")
            print(f"Phone: {student['phone']}")
            print(f"Major: {student['major']}")
            print(f"Estimated Graduation Year: {student['grad_year']}")
            print(f"GPA: {student['gpa']}")
            print(f"Classes:")
            for i, class_name in enumerate(student.get('classes', []), 1):
                print(f"  {i}. {class_name}")
            print("=" * 30)
        else:
            print(f"\nError: No student information to display.")

    # Finds the student if they exist based on their student id
    # Prints weather they are or are not found
    def query_student(self):
        id = input("Enter student ID to query: ")
        student = self.find_student(id)
        if student:
            print(f"\n{self.check_mark} Student found:")
            self.display_student(student)
            return True
        else:
            print(f"\n{self.cross_mark} Error: Student with ID {id} not found.")
            return False
    
    # Finds the user based on the student id if the id can't be found then
    # a user not found message is displayed
    def find_student(self, id):
        for student in self.students:
            if student['id'] == id:
                return student
        return None
    