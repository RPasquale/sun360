from flask import Flask, jsonify, request
from models import db, Incidence, Location, User, UVRecord, TempAlert,SSReminder, Mortality  # Import all models
from flask_sqlalchemy import SQLAlchemy
import os  # For environment variables 
# If we build any ML or AI models import below
#from your_ml_models import ClothingRecommender # Reminder to build clothing recommender

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')  # Load from environment variable
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Initialize SQLAlchemy

# Basic Routes (Placeholders )
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Sun360 API!'})

# LOCATIONS
@app.route('/locations', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()
    result = [loc.to_dict() for loc in all_locations]  
    return jsonify(result)

@app.route('/locations/<int:location_id>', methods=['GET']) 
def get_location(location_id):
    location = Location.query.get_or_404(location_id)

    # Include related data if needed
    result = location.to_dict()
    if request.args.get('include_suburbs'): 
        result['suburbs'] = [suburb.to_dict() for suburb in location.suburbs]
    # Add similar logic for other related data (temp_alerts, uv_records) as required

    return jsonify(result) 

# USERS
@app.route('/users', methods=['POST']) 
def create_user():
    data = request.get_json() 
    new_user = User(**data)  # Unpack data assuming it matches model attributes
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201  # Return created user, status code 201

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)  # Update attributes
        db.session.commit()
        return jsonify(user.to_dict())  

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', 204  # Return empty response, status code 204

# UV DATA (Simplified)
@app.route('/uv-data', methods=['GET'])
def get_uv_data():
    # Example: Get all UV records 
    uv_records = UVRecord.query.all()
    result = [record.to_dict() for record in uv_records]
    return jsonify(result) 

# SUNSCREEN REMINDERS
@app.route('/users/<int:user_id>/sunscreen-reminders', methods=['GET', 'POST'])
def manage_sunscreen_reminders(user_id):
    # Check if the user exists
    user = User.query.get_or_404(user_id)  

    if request.method == 'GET':
        reminders = user.ss_reminders  # Fetch reminders via relationship
        result = [reminder.to_dict() for reminder in reminders] 
        return jsonify(result)

    elif request.method == 'POST':
        data = request.get_json()
        new_reminder = SSReminder(user_id=user_id, **data)
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify(new_reminder.to_dict()), 201 

# Temp Alerts (assuming read-only)
# Routes for Temp Alerts
@app.route('/temp-alerts/<int:temp_alert_id>', methods=['GET'])
def get_temp_alert(temp_alert_id):
    temp_alert = TempAlert.query.get_or_404(temp_alert_id)
    return jsonify(temp_alert.to_dict())

@app.route('/locations/<int:location_id>/temp-alerts', methods=['GET'])
def get_temp_alerts_for_location(location_id):
    location = Location.query.get_or_404(location_id)

    # Include related data if needed
    result = location.to_dict()
    if request.args.get('include_temp_alerts'): 
        result['temp_alerts'] = [alert.to_dict() for alert in location.temp_alerts]  

    return jsonify(result) 

# Suburbs
@app.route('/locations/<int:location_id>/suburbs', methods=['GET'])
def get_suburbs_for_location(location_id):
    location = Location.query.get_or_404(location_id)  # Get the location
    suburbs = location.suburbs  # Fetch related suburbs via the relationship
    result = [suburb.to_dict() for suburb in suburbs]
    return jsonify(result)

# Mortality and Incidence 
@app.route('/mortality', methods=['GET'])
def get_mortality_data(): 
    # Filtering
    location_lat = request.args.get('lat') 
    location_long = request.args.get('long')
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    cancer_type = request.args.get('cancer_type')

    # Query Building
    query = Mortality.query
    if location_lat and location_long:
        # Example: Filter by a small range around a lat/long (adjust as needed)
        query = query.filter(Mortality.location_lat.between(location_lat - 0.1, location_lat + 0.1))
        query = query.filter(Mortality.location_long.between(location_long - 0.1, location_long + 0.1))
    if start_year and end_year:
        query = query.filter(Mortality.year.between(start_year, end_year))
    if cancer_type:
        query = query.filter(Mortality.cancer_type == cancer_type)

    mortality_records = query.all()
    result = [record.to_dict() for record in mortality_records]
    return jsonify(result)

# Incidence Routes
@app.route('/incidence', methods=['GET'])   
def get_incidence_data():
    # Filtering
    location_lat = request.args.get('lat') 
    location_long = request.args.get('long')
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    cancer_type = request.args.get('cancer_type')

    # Query Building
    query = Incidence.query
    if location_lat and location_long:
        # Example: Filter by a small range around a lat/long (adjust as needed)
        query = query.filter(Incidence.location_lat.between(location_lat - 0.1, location_lat + 0.1))
        query = query.filter(Incidence.location_long.between(location_long - 0.1, location_long + 0.1))
    if start_year and end_year:
        query = query.filter(Incidence.year.between(start_year, end_year))
    if cancer_type:
        query = query.filter(Incidence.cancer_type == cancer_type)

    incidence_records = query.all()
    result = [record.to_dict() for record in incidence_records]
    return jsonify(result)

# Current conditions for Locations
@app.route('/locations/<int:location_id>/current-conditions', methods=['GET'])
def get_current_conditions_for_location(location_id):
    location = Location.query.get_or_404(location_id)
    latest_uv_record = UVRecord.query.filter_by(location_id=location_id).order_by(UVRecord.uvrecord_timestamp.desc()).first()
    latest_temp_alert = TempAlert.query.filter_by(location_id=location_id).order_by(TempAlert.temp_alert_timestamp.desc()).first()
    latest_uv_record = UVRecord.query.filter_by(location_id=location_id).order_by(UVRecord.uvrecord_timestamp.desc()).first()

    result = {
        'location': location.to_dict(), 
        'uv_index': latest_uv_record.to_dict() if latest_uv_record else None,
        'temperature': latest_uv_record.temp_value if latest_uv_record else None,  
        'temperature_alert': latest_temp_alert.to_dict() if latest_temp_alert else None
    }
    return jsonify(result)


@app.route('/locations/<int:location_id>/temperature-history', methods=['GET'])
def get_temperature_history(location_id):
    start_date = request.args.get('start_date') 
    end_date = request.args.get('end_date')

    # Query for temperature records from your database (adjust as needed)
    if start_date and end_date:
        records = UVRecord.query.filter_by(location_id=location_id).filter(
                  UVRecord.uvrecord_timestamp.between(start_date, end_date)).all()
    else:
        # Fetch a default range (e.g., past 7 days)
        ... 

    result = [{'timestamp': record.uvrecord_timestamp, 'temperature': record.temp_value} 
              for record in records]
    return jsonify(result)



'''
#  Clothing Recommendations (Placeholder)
@app.route('/clothing-recommendations', methods=['POST'])
def get_clothing_recommendations():
    data = request.get_json()

    # Extract UV index, location, user data etc., from 'data' 
    # Example placeholders:
    uv_index = data.get('uv_index', 7)  # Default to a moderate UV index
    location = data.get('location', 'Melbourne, Australia')

    # Placeholder Recommendation Logic (replace later)
    recommendations = [
        {'clothing_type': 'Wide-brimmed hat', 'upf': 50},
        {'clothing_type': 'Sunglasses', 'upf': 400} 
    ]

    return jsonify(recommendations)
'''


# Run the App (Development Mode)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables 
    app.run(debug=True, port=5000) 
