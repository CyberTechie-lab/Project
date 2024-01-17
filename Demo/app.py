from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
current_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory,"test.db")}'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        #email = request.form['email']
        password = request.form['password']

       # Check if the username already exists
        existing_user = User.query.filter_by(username=username)
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            # Hash the password before storing
            hashed_password = generate_password_hash(password, method='base64')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
        print(f"Username: {username}")
        #print(f"Email: {email}")
        print(f"Password: {password}")

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            return 'Login Sucessfull!'
        else:
            flash('Login failed. Check your username and password.', 'error')

    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
Hi Test