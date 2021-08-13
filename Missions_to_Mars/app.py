from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Create an instance of Flask, be sure to pass __name__
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    db_info = mongo.db.mars_info.find_one()
    # Return template and data
    return render_template('index.html', mars_info=db_info)

# Route tha will trigger the scrape function
@app.route("/scrape")
def scraper():
    from scrape_mars import scrape

    info = scrape()

    mars_dict = mongo.db.mars_info
    mars_dict.drop()
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, info, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
