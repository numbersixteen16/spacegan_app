# Main backend logic will go here
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'spacegan_secret_key'

# Temporary user store (in-memory)
users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if username in users:
            flash('Username already exists.')
            return redirect(url_for('register'))

        users[username] = password
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_password = users.get(username)
        if user_password and check_password_hash(user_password, password):
            session['user'] = username
            return redirect(url_for('dashboard'))

        flash('Invalid credentials.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

import os
from werkzeug.utils import secure_filename
from PIL import Image
import io

# Create folders if not exist
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    file = request.files['image']
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('dashboard'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Mock enhancement for now (copying the same image)
    result_path = os.path.join(app.config['RESULT_FOLDER'], 'enhanced_' + filename)
    image = Image.open(file_path)
    image.save(result_path)

    return render_template('result.html', original=file_path, enhanced=result_path)

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)


