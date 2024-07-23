from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from flask_cors import CORS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from config import Config  # Import the Config class

app = Flask(__name__)
CORS(app)

# MongoDB client setup using the Config class
client = MongoClient(Config.MONGODB_URI)
db = client.national_parks_db

@app.route('/')
def home():
    return "Welcome to the National Parks API!"

# API endpoint to get amenities and activities
@app.route('/api/amenities_activities', methods=['GET'])
def get_amenities_activities():
    amenities_activities = list(db.Activities_and_Amenities_Collection.find({}, {'_id': 0}))
    return jsonify(amenities_activities)

# API endpoint to get entrance fees
@app.route('/api/entrance_fees', methods=['GET'])
def get_entrance_fees():
    entrance_fees = list(db.Entrance_Fees_Collection.find({}, {'_id': 0}))
    return jsonify(entrance_fees)

# API endpoint to get things to do
@app.route('/api/things_to_do', methods=['GET'])
def get_things_to_do():
    things_to_do = list(db.Things_to_Do_Collection.find({}, {'_id': 0}))
    return jsonify(things_to_do)

# API endpoint to get filtered parks based on user preferences
@app.route('/api/filtered_parks', methods=['POST'])
def get_filtered_parks():
    data = request.json
    amenities = data.get('amenities')
    activities = data.get('activities')
    season = data.get('season')
    preferred_weather = data.get('preferred_weather')

    # Perform filtering based on user preferences
    query = {}
    if amenities:
        query['amenity_name'] = {'$in': amenities}
    if activities:
        query['activity_name'] = {'$in': activities}
    if season:
        query['season'] = season
    if preferred_weather:
        query['min_summer_temp'] = {'$lte': preferred_weather['max_temp']}
        query['max_summer_temp'] = {'$gte': preferred_weather['min_temp']}

    filtered_parks = list(db.Activities_and_Amenities_Collection.find(query, {'_id': 0}))
    return jsonify(filtered_parks)

# API endpoint to get seaborn plot
@app.route('/api/seaborn_plot')
def seaborn_plot():
    df = pd.DataFrame(list(db.Activities_and_Amenities_Collection.find({}, {'_id': 0})))
    sns_plot = sns.scatterplot(x='min_summer_temp', y='max_summer_temp', data=df)
    img = BytesIO()
    sns_plot.figure.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render_template('seaborn_plot.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
