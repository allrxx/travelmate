from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database connection (uses DATABASE_URL environment variable if set)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://dhiya07:123%40dhiyaravi@my-postgres:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Redirect home to the login page
@app.route("/")
def home():
    return redirect(url_for("login"))

# Render the sign-up page
@app.route("/signin")
def signin():
    return render_template("signin.html")

# Render and process the login form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Check credentials (in production, use hashed passwords)
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return f"Welcome, {username}!"
        return "Invalid credentials", 401
    return render_template("login.html")

# Process the sign-up form
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    # Check if user already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return "User already exists", 400
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
