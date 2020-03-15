from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sample')
def sample():
    return render_template('sample.html')
