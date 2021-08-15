import json
from accountant import manager
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
manager.process()


def read_db():
    return manager.reader


def write_db():
    return manager.save()


@app.route("/")
def welcome():
    content = read_db()
    return render_template("index.html", content=content, stock=manager.stock, account=manager.account)


@app.route("/zakup/", methods=["GET", "POST"])
def buy():
    content = read_db()
    if request.method == "POST":
        manager.process_action("zakup", [request.form["Produkt"], request.form["Cena"], request.form["Ilosc"]])
        write_db()
        return redirect("/")
    return render_template("zakup.html", content=content)


@app.route("/sprzedaz/", methods=["GET", "POST"])
def sell():
    content = read_db()
    if request.method == "POST":
        manager.process_action("sprzedaz", [request.form["Produkt"], request.form["Cena"], request.form["Ilosc"]])
        write_db()
        return redirect("/")
    return render_template("sprzedaz.html", content=content)


@app.route("/saldo/", methods=["GET", "POST"])
def balance():
    content = read_db()
    if request.method == "POST":
        manager.process_action("saldo", [request.form["Kwota"], request.form["Komentarz"]])
        write_db()
        return redirect("/")
    return render_template("saldo.html", content=content)


@app.route("/historia/")
@app.route("/historia/<od>/")
@app.route("/historia/<od>/<do>/")
def history(od=None, do=None):
    if od and do:
        content = manager.history[int(od):int(do)]
        return render_template("historia.html", content=content)
    elif not do and od:
        content = manager.history[int(od):]
        return render_template("historia.html", content=content)
    else:
        content = manager.history
        return render_template("historia.html", content=content)


@app.route("/", methods=["GET", "POST"])
def main():
    content = read_db()
    if request.method == "POST":
        write_db()
        return redirect("/")
    return render_template("zakup.html", content=content)
