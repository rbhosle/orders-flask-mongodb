import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    uri = os.getenv("MONGODB_URI")


    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

    app.db = client.testdb


    @app.route("/", methods=["GET","POST"])
    def landing():
        entries = [(entry["name"], entry["price"]) for entry in app.db.testcoll.find({})]
        if request.method == "POST":
            item_name = request.form.get("itemName")
            item_price = request.form.get("itemPrice")
            entries.append((item_name, item_price))
            app.db.testcoll.insert_one({"name":item_name, "price":item_price})
            return redirect("/")
        return render_template("landing.html", entries=entries)

    @app.route("/summary", methods=["GET"])
    def summary():
        item_sum = sum([float(entry["price"]) for entry in app.db.testcoll.find({})]) 
        return render_template("summary.html", item_sum=item_sum)    


    return app

#  %23Passw0rd12%23%24
