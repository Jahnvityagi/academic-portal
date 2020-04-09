from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
from whitenoise import WhiteNoise
from datetime import datetime
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from tensorflow.keras.models import model_from_json
from spellchecker import SpellChecker
from nltk.corpus import wordnet as wn
from xml.etree import ElementTree
import uuid, os, json, dropbox, time, nltk, textstat, http.client, urllib.request, urllib.parse, urllib.error, docx
import numpy as np

lemmatizer = WordNetLemmatizer()

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'
API_KEY = 'BT1HAVEIyxAAAAAAAAAA-vYVvR_YifDzLeKTeYEAwAVCmqP17a2t3vEuQZGvjloV'
dbx_client = dropbox.Dropbox(API_KEY)
stopwords = nltk.corpus.stopwords.words('english')

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, f, file_to):
        dbx = dropbox.Dropbox(self.access_token)
        dbx.files_upload(f.read(), file_to)

transferData = TransferData(API_KEY)


_key = None

def setDefaultKey(key):
    global _key
    _key = key

def checkDocument(text, key=None):
    global _key
    if key is None:
        if _key is None:
            raise Exception('Please provide key as argument or set it using setDefaultKey() first')
        key = _key

    params = urllib.parse.urlencode({
        'key': key,
        'data': text,
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent':' python-ATD',
    }
    service = http.client.HTTPConnection("service.afterthedeadline.com")
    service.request("POST", "/checkDocument", body=params, headers=headers)
    response = service.getresponse()
    if response.status != http.client.OK:
        service.close()
        raise Exception('Unexpected response code from AtD service %d' % response.status)
    response_text = response.read()
    e = ElementTree.fromstring(response_text)
    service.close()
    errs = e.findall('message')
    if len(errs) > 0:
        raise Exception('Server returned an error: %s' % errs[0].text)
    return [Error(err) for err in e.findall('error')]

class Error:
    """ AtD Error Object"""
    def __init__(self, e):
        self.string = e.find('string').text
        self.description = e.find('description').text
        self.precontext = e.find('precontext').text
        self.type = e.find('type').text
        if not e.find('url') is None:
            self.url = e.find('url').text
        else:
            self.url = ""
        if not e.find('suggestions') is None:
            self.suggestions = [o.text for o in e.find('suggestions').findall('option')]
        else:
            self.suggestions = []
    def __str__(self):
        return "%s (%s)" % (self.string, self.description)

def getGrammarMistakes(essay):
    cnt = 0
    setDefaultKey('mygra2019#shs')
    errs=checkDocument(essay)
    for error in errs:
        if error.type=="grammar":
            cnt+=1
    return cnt

storage = {}
def getTopicCoherenceScore(essay_words, topic_words):
    score = 0
    for topic_word in topic_words:
        for essay_word in essay_words:
            myScore = 0
            if (topic_word,essay_word) not in storage:
                maximum_similarity = -1
                t_synset = wn.synsets(topic_word)
                s_synset = wn.synsets(essay_word)
                if (len (t_synset) != 0 and len (s_synset) != 0):
                    for synset_one in t_synset:
                        for synset_two in s_synset:
                            similarity = wn.path_similarity (synset_one,synset_two)
                            if similarity != None and similarity > maximum_similarity:
                                maximum_similarity = similarity
                                myScore += similarity
                score += myScore
                storage[(topic_word,essay_word)] = myScore
            else:
                score += storage[(topic_word,essay_word)]
    return score

def getAvgSentenceLength(sents):
    avg = 0
    tzr = nltk.tokenize.RegexpTokenizer(r'\w+')
    for s in sents:
        avg += len(tzr.tokenize(s))
    avg /= len(sents)
    return avg

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def generateSummary(notes):
    return notes

def generateAssignment(notes):
    return notes

def calculatePlagiarism(filename,uploads):
    tzr = nltk.tokenize.RegexpTokenizer(r'\w+')
    plagiarism = []
    dbx_client.files_download_to_file(filename, '/academic_portal_data/student_uploads/' + filename)
    if filename.endswith('.docx'):
        text = getText(filename)
    else:
        f = open(filename,'r')
        text = f.read()
    unique_words = set(tzr.tokenize(text))
    unique_words_ns1 = set()
    for word in unique_words:
        if word not in stopwords:
            unique_words_ns1.add(lemmatizer.lemmatize(word))
    os.remove(filename)
    for upload in uploads:
        if upload[0] == filename:
            continue
        dbx_client.files_download_to_file(upload[0], '/academic_portal_data/student_uploads/' + upload[0])
        if upload[0].endswith('.docx'):
            text = getText(upload[0])
        else:
            f = open(upload[0],'r')
            text = f.read()
        unique_words = set(tzr.tokenize(text))
        unique_words_ns2 = set()
        stopwords = nltk.corpus.stopwords.words('english')
        for word in unique_words:
            if word not in stopwords:
                unique_words_ns2.add(lemmatizer.lemmatize(word))
        intersection_len = len(unique_words_ns1.intersection(unique_words_ns2))
        union_len = len(unique_words_ns1.union(unique_words_ns2))
        plagiarism.append((((intersection_len / union_len)*100),upload[3]))
        os.remove(upload[0])
    plagiarism.sort(reverse = True)
    return plagiarism

@app.route('/getPlagiarism', methods=['POST'])
def getPlagiarism():
    roll_no = request.form['roll_no']
    filename = request.form['file']
    uuid = request.form['uuid']
    uploads = {}
    with open('student_uploads.json','r') as su:
        uploads = json.load(su)
    plag = calculatePlagiarism(filename,uploads[uuid])
    for upload in uploads[uuid]:
        if upload[3] == roll_no:
                upload[2] = plag
                break
    with open('student_uploads.json', 'w') as su:
        json.dump(uploads, su, indent=4)
    flash('Plagiarism Report generated successfully.')
    return redirect(url_for('teacher_dashboard'))

def calculateMarks(text, wordLimit, topic):
    features = []
    sents = nltk.tokenize.sent_tokenize(text)
    tzr = nltk.tokenize.RegexpTokenizer(r'\w+')
    essay_words = tzr.tokenize(text)
    topic_words = tzr.tokenize(topic)
    essay_words_ns = []
    topic_words_ns = []
    for word in essay_words:
        if word not in stopwords:
            essay_words_ns.append(word)
    for word in topic_words:
           if word not in stopwords:
               topic_words_ns.append(word)
    features.append(len(sents)) #sentenceLength
    features.append(len(essay_words_ns)) #wordLength
    spell = SpellChecker()
    features.append(len(spell.unknown(essay_words))) #spellingErrors
    features.append(getGrammarMistakes(text)) #grammarErrors
    features.append(getTopicCoherenceScore(essay_words_ns, topic_words_ns)) #topicCoherence
    features.append(getAvgSentenceLength(sents)) #avgSentLen
    features.append(len(set(essay_words_ns))) #uniqWords
    features.append(textstat.flesch_reading_ease(text)) #fleschReadingEase
    features.append(textstat.coleman_liau_index(text)) #CLIndex
    features.append(wordLimit)
    features = np.array([features])
    json_file = open('ffn_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("ffn_model.h5")
    pred = list(model.predict(features)[0])
    return pred.index(max(pred))


@app.route('/getMarks',methods=['POST'])
def getMarks():
    roll_no = request.form['roll_no']
    uuid = request.form['uuid']
    filename = request.form['file']
    wordLimit = request.form['wordLimit']
    topic = request.form['topic']
    uploads = {}
    with open('student_uploads.json','r') as su:
        uploads = json.load(su)
    dbx_client.files_download_to_file(filename, '/academic_portal_data/student_uploads/' + filename)
    if filename.endswith('.docx'):
        text = getText(filename)
    else:
        f = open(filename,'r')
        text = f.read()
    os.remove(filename)
    marks = calculateMarks(text, wordLimit, topic)
    for upload in uploads[uuid]:
        if upload[3] == roll_no:
            upload[1] = marks
            break
    with open('student_uploads.json', 'w') as su:
        json.dump(uploads, su, indent=4)
    flash('Marks generated successfully.')
    return redirect(url_for('teacher_dashboard'))

@app.route('/')
def home():
    return render_template('index.html')

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
    roll_no = request.form['rollno']
    print ("size=", os.path.getsize('student_credentials.json'))
    if os.path.getsize('student_credentials.json'):
        with open('student_credentials.json') as sc:
            credentials = json.load(sc)
    if email in credentials.keys():
        flash('An account with this email already exists. Please login.')
        return redirect(url_for('login_student'))
    else:
        credentials[email] = {
        'name' : full_name,
        'password' : pwd,
        'roll_no' : roll_no
        }
        with open('student_credentials.json', 'w') as sc:
            json.dump(credentials, sc, indent=4)
        session['StudentLoggedIn'] = True
        session['StudentEmail'] = email
        session['StudentRollNo'] = roll_no
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
            session['StudentRollNo'] = credentials[email]["roll_no"]
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
            summary_link, assignment_link = "NA", "NA"
            if notes[3] != "NA":
                summary_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_summaries/' + notes[0]).link
            if notes[4] != "NA":
                assignment_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_assignments/' + notes[0]).link
            timestamp = datetime_from_utc_to_local(dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes[0]).metadata.client_modified)
            notes_details.append([notes_link, summary_link, assignment_link, name, timestamp, filename])
    submissions = []
    student_uploads = {}
    if os.path.getsize('student_uploads.json'):
        with open('student_uploads.json') as su:
            student_uploads = json.load(su)
    if session["TeacherEmail"] in uploads and "essay_topics" in uploads[session['TeacherEmail']]:
        for topic in uploads[session['TeacherEmail']]["essay_topics"]:
            uuid = topic[3]
            name = topic[0]
            if uuid in student_uploads:
                for upload in student_uploads[uuid]:
                    date = datetime_from_utc_to_local(dbx_client.files_get_temporary_link('/academic_portal_data/student_uploads/' + upload[0]).metadata.client_modified)
                    file = dbx_client.files_get_temporary_link('/academic_portal_data/student_uploads/' + upload[0]).link
                    submissions.append([upload[3], name,date, upload[1],upload[2],file, upload[0], uuid, topic[2]])
    return render_template('teacher_dashboard.html', notes=notes_details, submissions = submissions)

@app.route('/teacher_notes')
def teacher_notes():
    teacher_email=request.args.get('teacher_email')
    with open('teacher_credentials.json') as tc:
        credentials = json.load(tc)
    details = credentials[teacher_email]
    uploads = {}
    if os.path.getsize('teacher_uploads.json'):
        with open('teacher_uploads.json') as tu:
            uploads = json.load(tu)
    notes_details = []
    if teacher_email in uploads and "notes" in uploads[teacher_email]:
        for notes in uploads[teacher_email]["notes"]:
            name = notes[2]
            filename = notes[0]
            notes_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes[0]).link
            summary_link, assignment_link = "NA", "NA"
            if notes[3] != "NA":
                summary_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_summaries/' + notes[0]).link
            if notes[4] != "NA":
                assignment_link = dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/generated_assignments/' + notes[0]).link
            timestamp = datetime_from_utc_to_local(dbx_client.files_get_temporary_link('/academic_portal_data/teacher_uploads/' + notes[0]).metadata.client_modified)
            notes_details.append([notes_link, summary_link, assignment_link, name, timestamp, filename])
    essay_topics = []
    if teacher_email in uploads and "essay_topics" in uploads[teacher_email]:
        for topics in uploads[teacher_email]["essay_topics"]:
            if datetime.strptime(topics[1], "%m/%d/%Y").date() >= datetime.today().date():
                student_uploads={}
                if os.path.getsize('student_uploads.json'):
                    with open('student_uploads.json') as su:
                        student_uploads = json.load(su)
                submitted = False
                if topics[3] in student_uploads:
                    for upload in student_uploads[topics[3]]:
                        if upload[3] == session['StudentRollNo']:
                            essay_topics.append([topics[0], topics[1], topics[2], topics[3], 'yes'])
                            submitted=True
                            break
                if not submitted:
                    essay_topics.append([topics[0], topics[1], topics[2], topics[3], 'no'])
    return render_template('teacher_notes.html', email= teacher_email,name=details['name'], spc = details['specialization'], dsg = details['designation'], notes=notes_details, topics = essay_topics)

@app.route('/upload_essay_topic', methods = ['POST'])
def upload_essay_topic():
    topic = request.form['topic']
    date = request.form['datepicker']
    limit = request.form['limit']
    email = session['TeacherEmail']
    uploads = {}
    if os.path.getsize('teacher_uploads.json'):
        with open('teacher_uploads.json') as tu:
            uploads = json.load(tu)
    if email not in uploads:
        uploads[email] = {}
    if "essay_topics" not in uploads[email]:
        uploads[email]["essay_topics"] = []
    id = str(uuid.uuid4())
    uploads[email]["essay_topics"].append([topic,date,limit,id])
    with open('teacher_uploads.json', 'w') as tu:
        json.dump(uploads, tu, indent=4)
    flash('Topic uploaded successfully.')
    return redirect(url_for('teacher_dashboard'))

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
    uploads[email]["notes"].append([notes.filename, exam, topic, "NA", "NA"])
    if os.path.getsize('teacher_uploads.json'):
        with open('teacher_uploads.json', 'w') as tu:
            json.dump(uploads, tu, indent=4)
    # summary_to = '/academic_portal_data/teacher_uploads/generated_summaries/' +  summary.filename
    # assignment_to = '/academic_portal_data/teacher_uploads/generated_assignments/' +  assignment.filename
    # transferData.upload_file(summary, summary_to)
    # transferData.upload_file(assignment, assignment_to)
    flash('Content uploaded successfully.')
    return redirect(url_for('teacher_dashboard'))

@app.route('/upload_answer', methods =['POST'])
def upload_answer():
    answer = request.files['file']
    uuid = request.form['uuid']
    email = request.form['email']
    file_to = '/academic_portal_data/student_uploads/' + answer.filename
    transferData.upload_file(answer, file_to)
    uploads = {}
    if os.path.getsize('student_uploads.json'):
        with open('student_uploads.json', 'r') as su:
            uploads = json.load(su)
    if uuid not in uploads:
        uploads[uuid] = []
    uploads[uuid].append([answer.filename, "NA", "NA", session['StudentRollNo']])
    with open('student_uploads.json', 'w') as su:
        json.dump(uploads, su, indent=4)
    flash('Uploaded successfully.')
    return redirect(url_for('teacher_notes', teacher_email=email))
