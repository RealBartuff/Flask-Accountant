
from accountant import manager
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

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
    account = db.Column(db.Integer, unique=False, nullable=False)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def welcome():
    stock = db.session.query(Stock).all()
    account = db.session.query(Account).filter(Account.id == 1).first()
    account = account.account if account else 0
    return render_template("index.html", stock=stock, account=account)


@app.route("/saldo/", methods=["GET", "POST"])
def balance():
    account = db.session.query(Account).filter(Account.id == 1).first()
    if request.method == "POST":
        if account.account + int(request.form["Kwota"]) < 0:
            raise Exception("Niewystarczające środki.")
        log = History(
            what_action="saldo",
            first_action=request.form["Kwota"],
            second_action=request.form["Komentarz"],
            third_action=None
        )
        account.account += int(request.form["Kwota"])
        db.session.add(log)
        db.session.add(account)
        db.session.commit()
        return redirect("/")
    return render_template("saldo.html")


@app.route("/zakup/", methods=["GET", "POST"])
def buy():
    account = db.session.query(Account).filter(Account.id == 1).first()
    if request.method == "POST":
        if account.account - (int(request.form["Cena"]) * int(request.form["Ilosc"])) < 0:
            raise Exception("Niewystarczające środki.")
        purchase = Stock(
            product=request.form["Produkt"],
            qty=request.form["Ilosc"]
        )
        db.session.add(purchase)
        account.account -= (int(request.form["Cena"]) * int(request.form["Ilosc"]))
        db.session.add(account)
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
    stock = db.session.query(Stock).filter(Stock.product).first()
    if request.method == "POST":
        if stock.product != request.form["Produkt"]:
            raise Exception("Brak towaru w magazynie.")
        sale = Stock(
            product=request.form["Produkt"],
            qty=request.form["Ilosc"]
        )
        account = db.session.query(Account).filter(Account.id == 1).first()
        stock.qty -= int(request.form["Ilosc"])
        db.session.add(sale)
        account.account += (int(request.form["Cena"]) * int(request.form["Ilosc"]))
        db.session.add(account)
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
    content = db.session.query(History).all()
    if od and do:
        x = db.session.query(Account).filter(Account.id == od).first()
        y = db.session.query(Account).filter(Account.id == do).last()
        content = x, y
        return render_template("historia.html", content=content)
    elif not do and od:
        content = db.session.query(Account).filter(Account.id == od).first()
        return render_template("historia.html", content=content)
    else:
        content = db.session.query(History).all()
        return render_template("historia.html", content=content)
