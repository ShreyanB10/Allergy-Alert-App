from urllib import response
import requests
import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pollen", methods=["POST"])
def pollen():
    if request.is_json:
        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")
        selected_allergies = data.get("selectedAllergies", [])
    else: 
         lat = request.form.get("lat")
         lon = request.form.get("lon")
         selected_allergies = request.form.getlist("selectedAllergies")

    if not lat or not lon:
        return jsonify({"error": "Missing latitude or longitude"}), 400
   
    url = (
      f"https://pollen.googleapis.com/v1/forecast:lookup?key={API_KEY}&location.longitude={lon}&location.latitude={lat}&days=1"
   )

    response = requests.get(url)
    if response.status_code != 200:
      return jsonify({"error": "Failed to fetch pollen data"}), 500
    
    print(response.status_code)
    print(response.text)

    api_data = response.json()

    daily_info = api_data["dailyInfo"][0]

    pollen_sum = []

    for pollen_type in daily_info["pollenTypeInfo"]:
        name = pollen_type.get("displayName")
        if selected_allergies and name.lower() not in [a.lower() for a in selected_allergies]:
            continue

        index_info = pollen_type.get("indexInfo", {})
        value = index_info.get("value", 0)
        category = index_info.get("category", "Unknown")
        description = index_info.get("indexDescription", "No description available")

        pollen_sum.append({
            "name": name,
            "value": value,
            "category": category,
            "description": description
        })
    if not pollen_sum:
        return jsonify({"error": "No pollen data available for the selected allergies"}), 404

        

    return jsonify({
           "data": daily_info["date"],
           "pollen": pollen_sum
    })


app.run(debug=True)
