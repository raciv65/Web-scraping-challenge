from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Instance of Flask app
app=Flask(__name__)

## Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

#Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
#Store the return value in Mongo as a Python dictionary
@app.route('/scrape')
def scrape():
    mars=mongo.db.mars
    data=scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)

if __name__=='__main__':
    app.run(debug=True)