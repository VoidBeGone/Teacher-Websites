import random
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy.orm.exc import NoResultFound


import os
import atexit



app = Flask(__name__)
app.config['SECRET_KEY'] = 'deb65a70153dfbf271b923f789e29d44f19bdad8473ca7291307e51c7a0648a9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
db_file_path = 'instance/app.db'

# Define your models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)


class Assignment(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False,primary_key=True)
    assignment_name = db.Column(db.String(120), nullable=False)
    assignment_weight = db.Column(db.Float, nullable=False)
    assignment_desc = db.Column(db.String(1000))


class assignment_student(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False,primary_key=True)
    user_id =  db.Column(db.Integer, unique=True, nullable=False)
    assignment_id =  db.Column(db.Integer, unique=True, nullable=False)
    grade = db.Column(db.Float, unique =False, nullable=True)



# Create the tables if they don't exist
with app.app_context():
    db.create_all()


        

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        # Generate random user ID

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user
        user = User(user_type=user_type, email=email, password=hashed_password, name=name)
        db.session.add(user)
        db.session.commit()

        # Save user type in session
        session['user_id'] = user.id
        session['user_type'] = user.user_type

        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to landing page if not logged in
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        try:
            user = User.query.filter_by(email=email).one()
            print(user)
            if bcrypt.check_password_hash(user.password, password):
                # Successful login
                session['user_id'] = user.id  # Save user ID in session
                session['user_type'] = user.user_type  # Save user type in session
                return 'Login successful', 200
            else:
                # Incorrect password
                return 'Incorrect email or password', 401
        except NoResultFound:
            # User not found
            return 'Incorrect email or password', 401
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('index'))

@app.route('/notes', methods=['GET', 'POST'])
def notes():
            return redirect(url_for('notes'))

@app.route('/add', methods=['GET', 'POST'])
def add():
        return render_template('add_sucess.html')

@app.route('/grades')
def grades():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to landing page if not logged in
    # Add your logic to fetch and display grades here
    return render_template('notes.html')

@app.route('/labs')
def labs():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to landing page if not logged in
    # Add your logic to fetch and display labs information here
    return render_template('labs.html')

@app.route('/assignments')
def assignments():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to landing page if not logged in
    # Add your logic to fetch and display labs information here
    # add_test_assignments()

    return render_template('assignments.html', context=Assignment.query.all())

@app.route('/anon-feedback')
def anon_feedback():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to landing page if not logged in
    # Add your logic to fetch and display labs information here
    return render_template('anon-feedback.html')
@app.route('/courseteam')
def courseteam():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to landing page if not logged in
    # Add your logic to fetch and display labs information here
    return render_template('courseteam.html')



def add_test_assignments():
    # Define test data for assignments
    test_assignments_data = [
        {"assignment_name": "Assignment 1", "assignment_weight": 10.0, "assignment_desc": "Description of Assignment 1"},
        {"assignment_name": "Assignment 2", "assignment_weight": 15.0, "assignment_desc": "Description of Assignment 2"},
        {"assignment_name": "Assignment 3", "assignment_weight": 20.0, "assignment_desc": "Description of Assignment 3"}
        # Add more test data as needed
    ]

    # Create Assignment objects from the test data
    assignments = []
    for assignment_data in test_assignments_data:
        assignment = Assignment(
            assignment_name=assignment_data["assignment_name"],
            assignment_weight=assignment_data["assignment_weight"],
            assignment_desc=assignment_data["assignment_desc"]
        )
        assignments.append(assignment)

    # Add the Assignment objects to the database session
    db.session.add_all(assignments)
    db.session.commit()

# Call the function to add test data to the Assignments table



if __name__ == '__main__':
    
    app.run(debug=True)