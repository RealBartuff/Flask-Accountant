import sys
from accountant import manager
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #test db to nazwa pliku w którym utworzymy bazę danych

db = SQLAlchemy(app)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_action = db.Column(db.Integer, unique=False)
    first_action = db.Column(db.Integer, unique=False)
    second_action = db.Column(db.String(120), unique=False)
    third_action = db.Column(db.Integer, unique=False)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64), unique=True)
    qty = db.Column(db.Integer, unique=False)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Integer, unique=False)


db.create_all()
"""manager.process()


def read_db():
    return manager.reader

def write_db():
    return manager.save()"""


@app.route("/", methods=["GET", "POST"])
def welcome():
    stock = db.session.query(Stock).all()
    funds = db.session.query(Account).filter(Account.id == 1).first()
    account = funds.account
    return render_template("index.html", stock=stock, account=account)


@app.route("/saldo/", methods=["GET", "POST"])
def balance():
    if request.method == "POST":
        if welcome.account + int(request.form["Kwota"]) < 0:
            raise Exception("Niewystarczające środki.")
        log = History(
            what_action="saldo",
            first_action=request.form["Kwota"],
            second_action=request.form["Komentarz"],
            third_action=None
        )
        val = welcome.account + int(request.form["Kwota"])
        db.session.add(log)
        db.session.add(val)
        db.session.commit()
        return redirect("/")
    return render_template("saldo.html")


@app.route("/zakup/", methods=["GET", "POST"])
def buy():
    if request.method == "POST":
        if welcome.account - (int(request.form["Cena"]) * int(request.form["Ilosc"])) < 0:
            raise Exception("Niewystarczające środki.")
        purchase = Stock(
            product=request.form["Produkt"],
            qty=request.form["Ilosc"]
        )
        db.session.add(purchase)
        val = welcome.account - (int(request.form["Cena"]) * int(request.form["Ilosc"]))
        db.session.add(val)
        log = History(
            what_action="zakup",
            first_action=request.form["Produkt"],
            second_action=request.form["Cena"],
            third_action=request.form["Ilosc"]
        )
        db.session.add(log)
        db.session.commit()
        return redirect("/")
    return render_template("zakup.html")


@app.route("/sprzedaz/", methods=["GET", "POST"])
def sell():
    if request.method == "POST":
        if int(welcome.stock.qty) - int(request.form["Ilosc"]) < 0:
            raise Exception("Za mało towaru w magazynie.")
        if request.form["Produkt"] not in welcome.stock.product:
            raise Exception("Brak towaru w magazynie.")
        sale = Stock(
            product=request.form["Produkt"],
            qty=request.form["Ilosc"]
        )
        welcome.stock.qty -= int(request.form["Ilosc"])
        db.session.add(sale)
        val = welcome.account + (int(request.form["Cena"]) * int(request.form["Ilosc"]))
        db.session.add(val)
        log = History(
            what_action="sprzedaz",
            first_action=request.form["Produkt"],
            second_action=request.form["Cena"],
            third_action=request.form["Ilosc"]
        )
        db.session.add(log)
        db.session.commit()
        return redirect("/")
    return render_template("sprzedaz.html")


@app.route("/historia/")
@app.route("/historia/<od>/")
@app.route("/historia/<od>/<do>/")
def history(od=None, do=None):
    history = db.session.query(History).all()
    if od and do:
        content = manager.history[int(od):int(do)]
        return render_template("historia.html", content=content)
    elif not do and od:
        content = manager.history[int(od):]
        return render_template("historia.html", content=content)
    else:
        content = manager.history
        return render_template("historia.html", content=content)
