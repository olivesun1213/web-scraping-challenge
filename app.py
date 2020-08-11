from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import ScrapeMars
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data=mongo.db.mars_data
    mars_info=ScrapeMars.scrape()
    

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)

