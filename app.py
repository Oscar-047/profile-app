from flask import Flask, render_template, request, redirect, url_for
from models import db, Profile

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///profile.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    name = request.form["name"]
    age = request.form["age"]
    city = request.form["city"]

    new_profile = Profile(name=name, age=age, city=city)
    db.session.add(new_profile)
    db.session.commit()

    return redirect(url_for("result"))

@app.route("/result")
def result():
    latest = Profile.query.order_by(Profile.id.desc()).first()
    return render_template("result.html", profile=latest)

if __name__ == "__main__":
    app.run(debug=True)