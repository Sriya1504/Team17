from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = '5f9d3c8e2a1b7f4d6e9c2b5a8d7f4e1c'  # Change this to a secure secret key

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Temporary data storage (replace with database in production)
students = {}
teachers = {}

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login decorators
def student_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'student':
            flash('Please login as student to access this page', 'error')
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'teacher':
            flash('Please login as teacher to access this page', 'error')
            return redirect(url_for('teacher_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    return render_template('home.html')

# Student Routes
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number')
        password = request.form.get('password')
        
        if roll_number in students and check_password_hash(students[roll_number]['password'], password):
            session['user_id'] = roll_number
            session['user_type'] = 'student'
            flash('Login successful!', 'success')
            return redirect(url_for('student_dashboard'))
        
        flash('Invalid roll number or password', 'error')
    return render_template('student_login.html')

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number')
        name = request.form.get('name')
        year = request.form.get('year')
        branch = request.form.get('branch')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if roll_number in students:
            flash('Roll number already registered', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            students[roll_number] = {
                'name': name,
                'year': year,
                'branch': branch,
                'password': generate_password_hash(password)
            }
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('student_login'))
            
    return render_template('student_signup.html')

@app.route('/student/dashboard')
@student_login_required
def student_dashboard():
    student_id = session.get('user_id')
    student = students[student_id]
    
    # Dummy marks data
    marks_data = [
        {
            'subject': 'Mathematics',
            'test_date': '2024-02-15',
            'max_marks': 100,
            'obtained_marks': 85
        },
        {
            'subject': 'Physics',
            'test_date': '2024-02-10',
            'max_marks': 100,
            'obtained_marks': 78
        },
        {
            'subject': 'Computer Science',
            'test_date': '2024-02-05',
            'max_marks': 100,
            'obtained_marks': 92
        }
    ]
    
    # Calculate statistics
    total_tests = len(marks_data)
    average_score = sum(m['obtained_marks'] for m in marks_data) / total_tests if total_tests > 0 else 0
    best_subject = max(marks_data, key=lambda x: x['obtained_marks'])['subject'] if marks_data else 'N/A'
    
    # Chart data
    performance_dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    performance_scores = [75, 82, 78, 85, 80]
    
    subjects = [mark['subject'] for mark in marks_data]
    subject_scores = [mark['obtained_marks'] for mark in marks_data]
    
    return render_template('student_dashboard.html',
                         student=student,
                         marks=marks_data,
                         total_tests=total_tests,
                         average_score=round(average_score, 1),
                         best_subject=best_subject,
                         performance_dates=json.dumps(performance_dates),
                         performance_scores=json.dumps(performance_scores),
                         subjects=json.dumps(subjects),
                         subject_scores=json.dumps(subject_scores))

# Teacher Routes
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        password = request.form.get('password')
        
        if teacher_id in teachers and check_password_hash(teachers[teacher_id]['password'], password):
            session['user_id'] = teacher_id
            session['user_type'] = 'teacher'
            flash('Login successful!', 'success')
            return redirect(url_for('teacher_dashboard'))
        
        flash('Invalid teacher ID or password', 'error')
    return render_template('teacher_login.html')

@app.route('/teacher/signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        name = request.form.get('name')
        department = request.form.get('department')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if teacher_id in teachers:
            flash('Teacher ID already registered', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            teachers[teacher_id] = {
                'name': name,
                'department': department,
                'password': generate_password_hash(password),
                'image_url': None
            }
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('teacher_login'))
            
    return render_template('teacher_signup.html')

@app.route('/teacher/dashboard')
@teacher_login_required
def teacher_dashboard():
    teacher_id = session.get('user_id')
    teacher = teachers[teacher_id]
    
    # Example data for charts
    performance_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    performance_data = [75, 80, 85, 82, 88]
    branch_labels = ['CS', 'ME', 'EE']
    branch_data = [45, 30, 25]

    # Sample student data
    students = [
        {
            'roll_number': '2020CS001',
            'name': 'John Doe',
            'branch': 'CS',
            'year': 2,
            'average_score': 85
        }
    ]

    return render_template('teacher_dashboard.html',
        teacher=teacher,
        students=students,
        total_students=len(students),
        average_score=85,
        top_performer='John Doe',
        performance_labels=performance_labels,
        performance_data=performance_data,
        branch_labels=branch_labels,
        branch_data=branch_data
    )

@app.route('/upload_image', methods=['POST'])
@teacher_login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{session['user_id']}_{int(datetime.now().timestamp())}.{file.filename.rsplit('.', 1)[1].lower()}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Update teacher's image URL
        teachers[session['user_id']]['image_url'] = url_for('static', filename=f'uploads/{filename}')
        
        return jsonify({
            'success': True,
            'image_url': teachers[session['user_id']]['image_url']
        })
    
    return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/get_analysis')
@teacher_login_required
def get_analysis():
    branch = request.args.get('branch')
    year = request.args.get('year')
    
    # Filter students based on branch and year
    filtered_students = [s for s in students.values() 
                        if (not branch or s['branch'] == branch) and 
                        (not year or s['year'] == int(year))]
    
    # Calculate statistics
    total = len(filtered_students)
    if total > 0:
        avg_score = sum(s.get('average_score', 0) for s in filtered_students) / total
        performance_data = {
            'total_students': total,
            'average_score': round(avg_score, 1),
            'branch_distribution': calculate_branch_distribution(filtered_students),
            'performance_trend': get_performance_trend()
        }
    else:
        performance_data = {
            'total_students': 0,
            'average_score': 0,
            'branch_distribution': {},
            'performance_trend': {}
        }
    
    return jsonify(performance_data)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))

# Helper functions for analysis
def calculate_branch_distribution(students_list):
    distribution = {}
    for student in students_list:
        branch = student['branch']
        distribution[branch] = distribution.get(branch, 0) + 1
    return distribution

def get_performance_trend():
    # Dummy data - replace with actual calculations
    return {
        'Jan': 75,
        'Feb': 78,
        'Mar': 82,
        'Apr': 79,
        'May': 85
    }

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File is too large'}), 413

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)