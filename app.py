import json
from manager import Manager, FileHandler
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

def read_db():
    with open("in.txt", "r") as f:
        content = f.read()
    return content

def write_db():
    return FileHandler.write_history

@app.route("/")
def welcome():
    content = read_db()
    return render_template("index.html", content=content)


"""@app.route("/names/<name>/")
def jaje(name):
    content = read_db()
    for row in content:
        if row["name"] != name:
            continue
        return row["profession"]
    return "Nie znaleziono"

@app.route("/main/", methods=["GET", "POST"])
def main():
    content = read_db()
    if request.method == "POST":
        content.append({"name": request.form["name"], "profession": request.form["profession"]})
        write_db(content)
        return redirect("/main/")
    #print(request.args["name"])
    #print(request.form["name"], request.form["profession"])
    return render_template("wzor-xml.html", content=content)"""




#w input type html może być number zamiast text
#min max i step do dodawania liczb, step nie jest konieczny