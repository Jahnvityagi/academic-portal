from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import uuid, os, json, dropbox

app = Flask(__name__)
app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'
API_KEY = ''
dbx_client = dropbox.Dropbox(API_KEY)

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, f, file_to):
        dbx = dropbox.Dropbox(self.access_token)
        dbx.files_upload(f.read(), file_to)

transferData = TransferData(API_KEY)

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
        return redirect(url_for('login_student'))
    credentials = {}
    full_name = request.form['first_name'] + " " + request.form['last_name']
    pwd = request.form['password']
    email = request.form['email']
    if os.path.getsize('student_credentials.json'):
        with open('student_credentials.json') as sc:
            credentials = json.load(sc)
    if email in credentials.keys():
        flash('An account with this email already exists. Please login.')
        return redirect(url_for('login_student'))
    else:
        credentials[email] = {
        'name' : full_name,
        'password' : pwd
        }
        with open('student_credentials.json', 'w') as sc:
            json.dump(credentials, sc, indent=4)
        session['StudentLoggedIn'] = True
        session['StudentEmail'] = email
        flash('You have been registered and logged in successfully.')
    return redirect(url_for('student_dashboard'))

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
            session['StudentLoggedIn'] = True
            session['StudentEmail'] = email
            return redirect(url_for('student_dashboard'))
        else:
            flash('Incorrect password. Please try again.')
    else:
        flash('No account with this email exists. Please Register to continue.')
    return redirect(url_for('login_student'))

@app.route('/student-logout')
def logout_student():
    session['StudentLoggedIn'] = False
    flash('Logged out successfully.')
    return redirect(url_for('login_student'))

@app.route('/login_teacher')
def login_teacher():
    return render_template('login_teacher.html')

@app.route('/register_teacher', methods = ['POST'])
def register_teacher():
    if request.form['password'] != request.form['password2']:
        flash('The passwords do not match. Please register again.')
        return redirect(url_for('login_teacher'))
    credentials = {}
    full_name = request.form['first_name'] + " " + request.form['last_name']
    pwd = request.form['password']
    email = request.form['email']
    spc = request.form['specialization']
    dsg = request.form['designation']
    if os.path.getsize('teacher_credentials.json'):
        with open('teacher_credentials.json') as tc:
            credentials = json.load(tc)
    if email in credentials.keys():
        flash('An account with this email already exists. Please login.')
        return redirect(url_for('login_teacher'))
    else:
        credentials[email] = {
        'name' : full_name,
        'password' : pwd,
        'specialization' : spc,
        'designation' : dsg
        }
        with open('teacher_credentials.json', 'w') as tc:
            json.dump(credentials, tc, indent=4)
        session['TeacherLoggedIn'] = True
        session['TeacherEmail'] = email
        flash('You have been registered and logged in successfully.')
    return redirect(url_for('teacher_dashboard'))

@app.route('/loginTeacher', methods = ['POST'])
def loginTeacher():
    email = request.form['email']
    pwd = request.form['password']
    credentials = {}
    if os.path.getsize('teacher_credentials.json'):
        with open('teacher_credentials.json') as tc:
            credentials = json.load(tc)
    if email in credentials.keys():
        if pwd == credentials[email]['password']:
            session['TeacherLoggedIn'] = True
            session['TeacherEmail'] = email
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Incorrect password. Please try again.')
    else:
        flash('No account with this email exists. Please Register to continue.')
    return redirect(url_for('login_teacher'))

@app.route('/teacher-logout')
def logout_teacher():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login_teacher'))

@app.route('/student_dashboard')
def student_dashboard():
    if not session.get('StudentLoggedIn'):
        flash('Please login to continue.')
        return redirect(url_for('login_student'))
    with open('student_credentials.json') as sc:
        credentials = json.load(sc)
    return render_template('student_dashboard.html', name = credentials[session['StudentEmail']]['name'])

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if not session.get('TeacherLoggedIn'):
        flash('Please login to continue.')
        return redirect(url_for('login_teacher'))
    uploads = {}
    if os.path.getsize('teacher_uploads.json'):
        with open('teacher_uploads.json') as tu:
            uploads = json.load(tu)
    notes_details = []
    if session["TeacherEmail"] in uploads and "notes" in uploads[session['TeacherEmail']]:
        for notes in uploads[session['TeacherEmail']]["notes"]:
            name = notes[2]
            filename = notes[0]
            notes_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes[0]).link
            summary_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_summaries/' + notes[0]).link
            assignment_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_assignments/' + notes[0]).link
            timestamp = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes[0]).metadata.client_modified
            notes_details.append([notes_link, summary_link, assignment_link, name, timestamp, filename])
    return render_template('teacher_dashboard.html', notes=notes_details)

@app.route('/teacher_notes')
def teacher_notes():
    teacher_email=request.args.get('teacher_email')
    with open('teacher_credentials.json') as tc:
        credentials = json.load(tc)
    details = credentials[teacher_email]
    return render_template('teacher_notes.html', name=details['name'], spc = details['specialization'], dsg = details['designation'])

def generateSummary(notes):
    return notes

def generateAssignment(notes):
    return notes


@app.route('/upload_teacher_notes', methods = ['POST'])
def upload_teacher_notes():
    if not session.get('TeacherLoggedIn'):
        flash('Please login to continue.')
        return redirect(url_for('login_teacher'))

    topic = request.form['topic']
    exam = request.form['exam']
    notes = request.files['file']
    file_to = '/academic_portal_data/teacher_uploads/' +  notes.filename
    transferData.upload_file(notes, file_to)
    email = session['TeacherEmail']
    uploads = {}
    if os.path.getsize('teacher_uploads.json'):
        with open('teacher_uploads.json') as tu:
            uploads = json.load(tu)
    if email not in uploads:
        uploads[email] = {}
    if "notes" not in uploads[email]:
            uploads[email]["notes"] = []
    uploads[email]["notes"].append([notes.filename, exam, topic])
    with open('teacher_uploads.json', 'w') as tu:
        json.dump(uploads, tu, indent=4)
    summary = generateSummary(notes)
    assignment = generateAssignment(notes)
    summary_to = '/academic_portal_data/teacher_uploads/generated_summaries/' +  summary.filename
    assignment_to = '/academic_portal_data/teacher_uploads/generated_assignments/' +  assignment.filename
    transferData.upload_file(summary, summary_to)
    transferData.upload_file(assignment, assignment_to)
    notes_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes.filename).link
    summary_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_summaries/' + notes.filename).link
    assignment_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_assignments/' + notes.filename).link
    timestamp = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes.filename).metadata.client_modified
    # notes_details = [notes_link, summary_link, assignment_link, topic, timestamp, notes.filename]
    # session['JustUploaded'] = notes_details
    flash('Uploaded successfully.')
    return redirect(url_for('teacher_dashboard'))
