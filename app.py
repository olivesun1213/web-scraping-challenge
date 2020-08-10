from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import ScrapeMars
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():

    mars=mongo.db.mars
    mars_data=ScrapeMars.scrape()

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)

