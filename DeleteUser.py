#this will delete a user that already exsists within the student.json file 
#this will also check which student to delete via ID

import json
from database import session, Student  # Add database import

#defining main method 
def delete_user():
    file_path = 'ProjectJSONs/student.json' #stdent.json file path
    
    try:
        # Load the student data from JSON
        with open(file_path, 'r') as file:
            data = json.load(file)
            students = data.get('students', []) #Students field
    except (FileNotFoundError, json.JSONDecodeError): #exception
        print("⚠️ Error: Unable to load student data. Make sure you have created a student already and Ensure the 'student.json' file exists and is correctly formatted.")
        return
    
    # User input for id
    student_id = input("Enter the Student ID to delete: ").strip()
    
    # Search for the student by ID
    student_to_delete = next((student for student in students if student['id'] == student_id), None)
    
    if not student_to_delete:
        print(f"⚠️ Error: No student found with ID {student_id}.")
        return

    #Displaying the students stats
    print("\nStudent Found!:")
    print(f"Name: {student_to_delete['name']}")
    print(f"ID: {student_to_delete['id']}")
    print(f"Phone: {student_to_delete['phone']}")
    print(f"Major: {student_to_delete['major']}")

    #Simple confirmation to delete user
    confirm = input("Are you sure you want to delete this student? (Y/N): ").strip().upper() #Get rid of whitespace and makes it capital
    if confirm not in ['Y', 'YES']:  #yes or y
        print("Deletion canceled." )
        return

    try:
        # Delete from database first then json will be after
        student_db = session.query(Student).filter_by(id=student_id).first()
        if student_db:
            session.delete(student_db)
            session.commit()

        #Remove from JSON
        students.remove(student_to_delete)
        
        # Write back to the student.json file correctly!
        with open(file_path, 'w') as file:
            json.dump({'students': students}, file, indent=4)
        
        print("✅ Success! The student has been deleted from the database.")
    
    except Exception as e:
        session.rollback()  #Rollback method if something goes wrong
        print(f"❌ Error: Unable to complete deletion. {str(e)}")


