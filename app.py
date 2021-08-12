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
    # return str(request.form)
    content = read_db()
    if request.method == "POST":
        manager.process_action("zakup", [request.form["Produkt"], request.form["Cena"], request.form["Ilosc"]])
        write_db()
    return render_template("zakup.html", content=content)


@app.route("/sprzedaz/")
def sell():
    return render_template("sprzedaz.html")


@app.route("/saldo/")
def balance():
    return render_template("saldo.html")


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
        # content.append({"name": request.form["name"], "profession": request.form["profession"]})
        write_db()
        return redirect("/")
    #print(request.args["name"])
    #print(request.form["name"], request.form["profession"])
    return render_template("zakup.html", content=content)




#w input type html może być number zamiast text
#min max i step do dodawania liczb, step nie jest konieczny

"""@app.route("/names/<name>/")
def jaje(name):
    content = read_db()
    for row in content:
        if row["name"] != name:
            continue
        return row["profession"]
    return "Nie znaleziono"""