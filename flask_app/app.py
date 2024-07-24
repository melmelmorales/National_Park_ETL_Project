from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import folium
from folium.plugins import MarkerCluster
from dotenv import load_dotenv
import os
import logging

app = Flask(__name__)
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client['national_parks_db']

# Function to create a map with parks
def create_map(parks):
    m = folium.Map(location=[48.8566, -121.5059], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(m)

    for park in parks:
        popup_content = f"<strong>{park['park_name']}</strong><br>"
        popup_content += f"<a href='{park['park_url']}' target='_blank'>Park Website</a><br>"
        if park.get('free_park', 'False') == 'True':
            popup_content += "Free Park<br>"
        else:
            if park.get('total_fees'):
                popup_content += f"Total Fees: ${park['total_fees']}<br>"
            if park.get('pass_fee'):
                popup_content += f"Pass Fee: ${park['pass_fee']}<br>"
            popup_content += f"<a href='{park.get('fees_url', '#')}' target='_blank'>Fees Info</a><br>"
        popup_content += f"Summer Temp: {park.get('min_summer_temp')} - {park['max_summer_temp']} °F<br>"
        popup_content += f"Winter Temp: {park.get('min_winter_temp')} - {park['max_winter_temp']} °F<br>"
        popup_content += f"Spring Temp: {park.get('min_spring_temp')} - {park.get('max_spring_temp')} °F<br>"
        popup_content += f"Fall Temp: {park.get('min_fall_temp')} - {park.get('max_fall_temp')} °F<br>"

        folium.Marker(
            location=[float(park['park_latitude']), float(park['park_longitude'])],
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(marker_cluster)

    return m._repr_html_()

@app.route('/')
def index():
    # Fetch unique amenities and activities
    amenities = list(db['Amenities_Collection'].distinct("amenity_name"))
    activities = list(db['Activities_Collection'].distinct("activity_name"))

    # Fetch all parks for initial map display
    all_parks = list(db['Activities_and_Amenities_Collection'].find({}, {"_id": 0}))
    map_html = create_map(all_parks)

    return render_template('index.html', amenities=amenities, activities=activities, map_html=map_html)

@app.route('/filter_parks', methods=['POST'])
def filter_parks():
    data = request.json
    selected_amenities = data.get('selected_amenities', [])
    selected_activities = data.get('selected_activities', [])
    selected_season = data.get('selected_season', 'summer')

    # Determine temperature fields based on selected season
    season_temp_fields = {
        'summer': ('min_summer_temp', 'max_summer_temp'),
        'winter': ('min_winter_temp', 'max_winter_temp'),
        'spring': ('min_spring_temp', 'max_spring_temp'),
        'fall': ('min_fall_temp', 'max_fall_temp')
    }
    min_temp_field, max_temp_field = season_temp_fields[selected_season]

    query = {}
    if selected_amenities:
        query['amenity_name'] = {'$in': selected_amenities}
    if selected_activities:
        query['activity_name'] = {'$in': selected_activities}

    logging.debug(f"Filter Query: {query}")

    # Fetch parks matching the criteria
    matching_parks = list(db['Activities_and_Amenities_Collection'].find(query, {"_id": 0}))

    logging.debug(f"Matching Parks: {matching_parks}")

    # Create map with the filtered parks
    map_html = create_map(matching_parks)
    return jsonify({'map_html': map_html})

if __name__ == "__main__":
    app.run(debug=True)
