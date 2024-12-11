'''
This is the class file that will be used to modify a students information
'''
#our imports
import json
import re
from database import session, Student  # Add database import
import os

class ModifyStudent:
    #Start of the constuct modifier
    def __init__(self, json_file='ProjectJSONs/student.json'):  #calling through out file directory
        self.json_file = json_file
        if not os.path.exists(self.json_file):
            print("⚠️ File not found at: {self.json_file}")
            try:
                os.makedirs('ProjectJSONs', exist_ok=True)  #Creating directory if it doesnt work
            except Exception as e:
                print(f"❌ Error creating directory: {e}")
        
        self.students = self.load_students()
        #Here are some emjois in unicode
        self.check_mark = "\u2705"
        self.envelope = "\u2709"  
        self.cross_mark = "\u274C"  
        self.telephone = "\u260E"

    # Loading the student method
    def load_students(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                students = data.get('students', [])
                return students
        except FileNotFoundError:
            return []

    # Gets user prompts, however, if the user enters nothing it keeps it the same, neat-o
    def get_input(self, prompt, current_value):
        user_input = input(prompt)
        return user_input if user_input else current_value

    # Finds the user based on the student id if the id can't be found then
    # a user not found message is displayed
    def find_student(self, id):
        # Convert input id to string to match JSON format
        id = str(id)
        for student in self.students: # Access the students list directly
            if student['id'] == id:
                return student
        return None
    
    # Method used to modify the student information
    def modify_student(self):
        # Gets a search student id from the user
        id = input("\nEnter the Student ID to modify: ")
        student = self.find_student(id)
        if not student:
            print(f"\n{self.cross_mark} Error: Student ID {id} not found.")
            return False

        # Calls the display student method
        self.display_student(student)
        
        # Store original values
        original_values = student.copy()

        # New prompts to get user modifications
        fields = [
            ('id', "\nEnter a new student ID 6 digits long starting with 700 (press Enter to keep current): "),
            ('name', "\nEnter new name with first and last name capitalized (press Enter to keep current): "),
            ('phone', "\nEnter new phone (XXX-XXX-XXXX) (press Enter to keep current): "),
            ('major', "\nEnter new major (SE, CS, CYBR, IT, DS) (press Enter to keep current): "),
            ('gpa', "\nEnter new GPA (0.1-4.0) (press Enter to keep current): ")
        ]

        # Get and validate new values
        for field, prompt in fields:
            while True:
                new_value = self.get_input(prompt, student[field])
                if new_value == student[field] or self.validate_field(field, new_value):
                    student[field] = new_value
                    break
                print(f"\n{self.cross_mark} Invalid {field} format. Please try again.")

        try:
            # Update JSON
            with open(self.json_file, 'w') as file:
                for i, s in enumerate(self.students):
                    if s['id'] == original_values['id']:
                        self.students[i] = student
                        break
                json.dump({'students': self.students}, file, indent=4)

            # Update database
            student_db = session.query(Student).filter_by(id=original_values['id']).first()
            if student_db:
                student_db.id = student['id']
                student_db.name = student['name']
                student_db.phone = student['phone']
                student_db.major = student['major']
                student_db.gpa = float(student['gpa'])
                session.commit()
            
            print(f"\n{self.check_mark} Student information updated successfully!" )
            return True
            
        except Exception as e:
            session.rollback()
            print(f"\n⚠️ Error updating student information: {str(e)}")
            return False

    # Update the validate_field method to include GPA validation
    def validate_field(self, field, value):
        if field == 'id':
            return re.match(r'^700\d{3}$', value) is not None
        elif field == 'name':
            return re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', value) is not None
        elif field == 'phone':
            return re.match(r'^\d{3}-\d{3}-\d{4}$', value) is not None
        elif field == 'major':
            return value.upper() in ['SE', 'CS', 'DS', 'IT', 'CYBR']
        elif field == 'gpa':
            try:
                gpa = float(value)
                return 0.1 <= gpa <= 4.0
            except ValueError:
                return False
        return False

    # Update the display_student method to show GPA
    def display_student(self, student):
        if student:
            print("\n" + "=" * 30)
            print(f"Student Information:")
            print(f"ID:    {student['id']}")
            print(f"Name:  {student['name']}")
            print(f"Phone: {student['phone']}")
            print(f"Major: {student['major']}")
            print(f"GPA:   {student['gpa']}")  # Added GPA display
            print(f"Estimated Graduation Year: {student['grad_year']}")
            print(f"Classes:")
            for i, class_name in enumerate(student.get('classes', []), 1):
                print(f"  {i}. {class_name}")
            print("=" * 30)
        else:
            print(f"\n⚠️ Error: No student information to display.")