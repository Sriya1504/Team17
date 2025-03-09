from app import db, Student, StudentMarks
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def add_test_data():
    # Add multiple students
    students_data = [
        {
            'roll_number': '2020CS001',
            'name': 'John Doe',
            'year': 2,
            'branch': 'Computer Science',
            'email': 'john.doe@university.com',
            'password': 'password123'
        },
        {
            'roll_number': '2020CS002',
            'name': 'Jane Smith',
            'year': 2,
            'branch': 'Computer Science',
            'email': 'jane.smith@university.com',
            'password': 'password123'
        }
    ]

    subjects = [
        'Data Structures',
        'Database Management',
        'Computer Networks',
        'Operating Systems',
        'Software Engineering'
    ]

    for student_info in students_data:
        student = Student(
            roll_number=student_info['roll_number'],
            name=student_info['name'],
            year=student_info['year'],
            branch=student_info['branch'],
            email=student_info['email'],
            password=generate_password_hash(student_info['password'])
        )
        db.session.add(student)
        db.session.commit()

        # Add marks for each student
        for subject in subjects:
            for i in range(3):
                test_date = datetime.now() - timedelta(days=random.randint(1, 90))
                mark = StudentMarks(
                    student_id=student.id,
                    subject=subject,
                    test_date=test_date,
                    max_marks=100,
                    obtained_marks=random.randint(65, 98)
                )
                db.session.add(mark)
        
        db.session.commit()
    print("Test data added successfully!")

if __name__ == '__main__':
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create new tables
        db.create_all()
        # Add test data
        add_test_data()