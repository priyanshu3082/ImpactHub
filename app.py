from os import environ
from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#app.secret_key = os.urandom(24).hex()
#app.config[b'\xc2\xac\x91-\xe5\x1b\x7f\xb5\x11\x8c+\xcb)\x92\x82\xbc\x85r\xa0Q&\xac0h'] = environ.get(b'\xc2\xac\x91-\xe5\x1b\x7f\xb5\x11\x8c+\xcb)\x92\x82\xbc\x85r\xa0Q&\xac0h')
app.secret_key = b'\xc2\xac\x91-\xe5\x1b\x7f\xb5\x11\x8c+\xcb)\x92\x82\xbc\x85r\xa0Q&\xac0h'
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50), nullable=False)  # Add role to User model

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    progress = db.Column(db.Text)  # Field to track what the child has learned

    def __init__(self, name, category, volunteer_id, progress=''):
        self.name = name
        self.category = category
        self.volunteer_id = volunteer_id
        self.progress = progress

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    adhar_card_number = db.Column(db.String(12), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, address, adhar_card_number, phone_number):
        self.name = name
        self.age = age
        self.address = address
        self.adhar_card_number = adhar_card_number
        self.phone_number = phone_number

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/Contact")
def contact():
    return render_template("contact.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if session.get('email'):
        user = User.query.filter_by(email=session['email']).first()
        if user.role == 'Volunteer':
            children = Child.query.filter_by(volunteer_id=user.id).all()
            return render_template('dashboard.html', user=user, children=children)
        return render_template('dashboard.html', user=user)
    
    return redirect('/login')

@app.route('/register_child', methods=['GET', 'POST'])
def register_child():
    if session.get('email'):
        user = User.query.filter_by(email=session['email']).first()
        if user.role != 'Volunteer':
            return "Access Denied"

        if request.method == 'POST':
            name = request.form['name']
            category = request.form['category']
            role = request.form['role']
            new_child = Child(name=name, category=category, volunteer_id=user.id)
            db.session.add(new_child)
            db.session.commit()
            return redirect('/dashboard')

        return render_template('register_child.html')
    return redirect('/login')

@app.route('/track_progress/<int:child_id>', methods=['GET', 'POST'])
def track_progress(child_id):
    if session.get('email'):
        user = User.query.filter_by(email=session['email']).first()
        if user.role != 'Volunteer':
            return "Access Denied"

        child = Child.query.get(child_id)
        if request.method == 'POST':
            progress = request.form['progress']
            child.progress += f"\n{progress}"
            db.session.commit()
            return redirect('/dashboard')

        return render_template('track_progress.html', child=child)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
