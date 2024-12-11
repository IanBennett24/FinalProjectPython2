import json

class ShowStudent:
    # The costructor method
    def __init__(self, json_file):
        self.json_file = json_file
        self.students = self.load_students()
        
        self.check_mark = "\u2705"
        self.envelope = "\u2709"  
        self.cross_mark = "\u274C"  
        self.telephone = "\u260E"

    # Method that loads the students from the file
    def load_students(self):
        try:
            with open('ProjectJSONs/student.json', 'r') as f:
                data = json.load(f)
                students = data.get('students', [])
                if not students:
                    print("\n ⚠️ Warning: No students found in JSON file")
                return students
            
        except json.JSONDecodeError as e:
            print("\n ⚠️ Error: Invalid JSON format in file: {str(e)}")
            return []
        except Exception as e:
            print(f"\n ⚠️ Error reading file! Please Make Sure you have created a student already!: {str(e)}")
            return []

    # The menu to give the user search options
    def search_by_menu(self):
        while True:
            print("\n=== Student Management System ===")
            print("1. Show All Students")
            print("2. Search by Name")
            print("3. Search by ID")
            print("4. Search by Major")
            print("Enter to Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.display_all_students()
            elif choice == '2':
                self.search_by_name()
            elif choice == '3':
                self.search_by_id()
            elif choice == '4':
                self.filter_by_major()
            elif choice == '':
                print("Goodbye!")
                break
            else:
                print("\n❌Invalid choice. Please try again.")

    # Method to print out students individually
    def display_student(self, student):
        if student:
            print(f"{student['id']:<12}"
                f"{student['name']:<15}"
                f"{student['age']:<5}"
                f"{student['gender']:<8}"
                f"{student['major']:<8}"
                f"{student['gpa']:<7}"
                f"{student['phone']:<15}")

    # 1. Show all students
    # Method to display all of the students
    def display_all_students(self):
        print("=" * 60)
        print(f"{'ID':<12}{'Name':<15}{'Age':<5}{'Gender':<8}{'Major':<8}{'GPA':<7}{'Phone':<15}")
        print("=" * 60)
    
        if not self.students:
            print("\n❌ No students found.")
            return
        
        for student in self.students:
            print(f"{student['id']:<12}"
                f"{student['name']:<15}"
                f"{student['age']:<5}"
                f"{student['gender']:<8}"
                f"{student['major']:<8}"
                f"{student['gpa']:<7}"
                f"{student['phone']:<15}")
    
        print("=" * 60)

    # 2. Search by Name
    # Method that allows the user to search the database by name 
    def search_by_name(self):
        name = input("\nEnter student name to search: ").strip().upper()
        found = False
        print("=" * 60 )
        print(f"{'ID':<12}{'Name':<15}{'Age':<5}{'Gender':<8}{'Major':<8}{'GPA':<7}{'Phone':<15}")
        print("=" * 60)
        for student in self.students:
            if student['name'].upper().find(name) != -1:
                self.display_student(student)
                found = True
        if not found:
            print(f"\n❌ No students found with name containing '{name}'")

    # 3. Search by ID
    # Method that allows the user to search by the id
    def search_by_id(self):
        student_id = input("\nEnter student ID: ").strip()
        found = False
        print("=" * 60)
        print(f"{'ID':<12}{'Name':<15}{'Age':<5}{'Gender':<8}{'Major':<8}{'GPA':<7}{'Phone':<15}")
        print("=" * 60)
        for student in self.students:
            if student['id'] == student_id:
                self.display_student(student)
                found = True
                break
        if not found:
            print(f"\n❌ No student found with ID: {student_id}")

    # 4. Search by major
    # Method that allows the user to earch by major
    def filter_by_major(self):
        print("\nAvailable majors:")
        majors = set(student['major'] for student in self.students)
        for major in majors:
            print(f"* {major}")
        while True:
            major = input("\nEnter the major to filter by (or press Enter to see all students): ").strip().upper()
            print(f"\n=== {major} Students ===")
            print("=" * 60)
            print(f"{'ID':<12}{'Name':<15}{'Age':<5}{'Gender':<8}{'Major':<8}{'GPA':<7}{'Phone':<15}")
            print("=" * 60)
            if not major:
                self.display_all_students()
                break
            elif major.upper() in {m.upper() for m in majors}:
                self.display_filtered_students(major)
                break
            else:
                print("\n❌ Invalid major. Please try again.")
    # Method that filters the students by their major
    def display_filtered_students(self, major=None):
        filtered_students = self.students
        if major:
            filtered_students = [student for student in self.students 
                               if student['major'].upper() == major.upper()]
        if not filtered_students:
            print(f"\n❌ No students found" + (f" with major {major}." if major else "."))
            return
        for student in filtered_students:
            self.display_student(student)

    

 
