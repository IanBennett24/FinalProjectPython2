#This is the database file that will handle all our database operations for storing student and admin data
#Make sure you have SQLAlchemy downloaded or it wont work: pip install sqlalchemy

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
import json  # Add import for JSON handling

#create teh base class
Base = declarative_base()

#create the engine object to create the db if it does not exsist
#echo flag will give real time
engine = create_engine('sqlite:///StudentManagement.db',echo = False)

#student class
class Student(Base):# I renamed Professor Minzeys class
    #creat the table student 
    __tablename__ = 'Student'
    #Columns within student table
    id = Column(String(9), primary_key = True, unique = True)
    name = Column(String(32), nullable = False)
    age = Column(Integer)
    gender = Column(String(1))
    major = Column(String(32))
    phone = Column(String(32))
    gpa = Column(Float) #since gpa have floating points

#user class
class AdminInfo(Base):
    #create table user
    __tablename__ = 'Admin_Info'
    #columns within user table
    name = Column(String(32), primary_key = True, nullable = False)
    password = Column(String(512))

#Add all the tables into the db if they do not exsist
Base.metadata.create_all(engine)

#Creates a session object to initiate different executables to teh db
Session = sessionmaker(bind = engine)
session = Session()

# Function to load student data from JSON
def load_students_from_json():
    with open('ProjectJSONs/student.json', 'r') as file:
        data = json.load(file)
        for student in data['students']:
            # Create Student object for each student in JSON
            s = Student(
                id=student['id'],
                name=student['name'],
                age=student['age'],
                gender=student['gender'],
                major=student['major'],
                phone=student['phone'],
                gpa=student['gpa']
            )
            session.merge(s)  #using the merge method

#loading admin data 
def load_admin_from_json():
    with open('ProjectJSONs/admin.json', 'r') as file:
        data = json.load(file)
        for admin in data['admin']:
            # Create User object for each admin in JSON
            u = AdminInfo(
                name=admin['id'],
                password=admin['password']
            )
            session.merge(u)  # merge will update if exists, insert if doesn't
    session.commit()
'''#We can un comment this to make sure our stuff is working, watch Professor Minzeys video for questions
# Load data from JSON files
try:
    print("Loading student data...")
    load_students_from_json()
    print("Loading admin data...")
    load_admin_from_json()
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {str(e)}")
    session.rollback()
# Verify the data was loaded
print("\nStudents in database:")
students = session.query(Student).all()
for student in students:
    print(f"Name: {student.name} | Major: {student.major} | ID: {student.id}")

print("\nAdmins in database:")
admins = session.query(AdminInfo).all()
for admin in admins:
    print(f"Username: {admin.name}")
'''