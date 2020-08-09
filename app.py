from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import ScrapeMars
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = ScrapeMars.scrape_News()
    mars_data = ScrapeMars.scrape_Image()
    mars_data = ScrapeMars.scrape_Facts()
    mars_data = ScrapeMars.scrape_Hemisphere()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

