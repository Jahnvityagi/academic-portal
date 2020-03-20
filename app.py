from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import uuid, os, json, ast

app = Flask(__name__)
app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login_student')
def login_student():
    return render_template('login_student.html')

@app.route('/register_student', methods = ['POST'])
def register_student():
    if request.form['password'] != request.form['password2']:
        flash('The passwords do not match. Please register again.')
    else:
        credentials = {}
        full_name = request.form['first_name'] + " " + request.form['last_name']
        pwd = request.form['password']
        email = request.form['email']
        if os.path.getsize('student_credentials.json'):
            with open('student_credentials.json') as sc:
                credentials = json.load(sc)
        credentials[email] = {
        'name' : full_name,
        'password' : pwd
        }
        with open('student_credentials.json', 'w') as sc:
            json.dump(credentials, sc, indent=4)
        flash('Registered successfully. Please login to continue.')
    return redirect(url_for('login_student'))

@app.route('/loginStudent', methods = ['POST'])
def loginStudent():
    email = request.form['email']
    pwd = request.form['password']
    credentials = {}
    if os.path.getsize('student_credentials.json'):
        with open('student_credentials.json') as sc:
            credentials = json.load(sc)
    if email in credentials.keys():
        if pwd == credentials[email]['password']:
            session['LoggedIn'] = True
            session['email'] = email
            flash('Logged in successfully.')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Incorrect password. Please try again.')
    else:
        flash('No account with this email exists. Please Register to continue.')
    return redirect(url_for('login_student'))

@app.route('/login_teacher')
def login_teacher():
    return render_template('login_teacher.html')

@app.route('/student_dashboard')
def student_dashboard():
    if not session.get('LoggedIn'):
        flash('Please login to continue.')
        return redirect(url_for('login_student'))
    with open('student_credentials.json') as sc:
        credentials = json.load(sc)
    return render_template('student_dashboard.html', name = credentials[session['email']]['name'])

@app.route('/student-logout')
def logout_student():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login_student'))


@app.route('/upload_content')
def upload_content():
    return render_template('upload_content.html')

@app.route('/view_content')
def view_content():
    return render_template('view_content.html')

@app.route('/view_submission')
def view_submission():
    return render_template('view_submission.html')

@app.route('/ela_notes')
def ela_notes():
    return render_template('ela_notes.html')
