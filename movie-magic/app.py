
from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid

app = Flask(__name__)
app.secret_key = "secret123"

users = {}
bookings = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if username in users:
            flash("User already exists")
            return redirect(url_for("signup"))

        users[username] = {"email":email,"password":password}
        flash("Registration successful")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("home1"))
        else:
            flash("Invalid login")

    return render_template("login.html")

@app.route('/home1')
def home1():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home1.html")

@app.route('/booking')
def booking():
    if "user" not in session:
        return redirect(url_for("login"))

    movie = request.args.get("movie")
    theatre = request.args.get("theatre")
    price = request.args.get("price")

    return render_template("b1.html", movie=movie, theatre=theatre, price=price)

@app.route('/tickets', methods=["POST"])
def tickets():
    if "user" not in session:
        return redirect(url_for("login"))

    movie = request.form["movie"]
    theatre = request.form["theatre"]
    seats = request.form["seats"]
    price = request.form["price"]

    booking_id = str(uuid.uuid4())[:8]

    booking = {
        "id":booking_id,
        "user":session["user"],
        "movie":movie,
        "theatre":theatre,
        "seats":seats,
        "price":price
    }

    bookings.append(booking)

    return render_template("tickets.html", booking=booking)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact_us')
def contact():
    return render_template("contact_us.html")

@app.route('/logout')
def logout():
    session.pop("user",None)
    flash("Logged out")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
