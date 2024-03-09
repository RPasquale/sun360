from flask import Flask, jsonify, request
import psycopg2
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from faker import Faker
from flask_cors import CORS

import os  # For environment variables
# If we build any ML or AI models import below
# from your_ml_models import ClothingRecommender # Reminder to build clothing recommender

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# Database Configuration
conn = psycopg2.connect(
    "postgresql://ta11:Ma5sm0_QVsBHDEVrk0LJuw@sun360-1974.g8x.gcp-southamerica-east1.cockroachlabs.cloud:26257/sun360?sslmode=verify-full")


@app.teardown_appcontext
def close_database_connection():
    conn.close()


CORS(app)

# Basic Routes (Placeholders )


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Sun360 API!'})


# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # hashing passwords
    if user and check_password_hash(user.hashed_password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# LOGOUT


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200


# USERS
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    cur = conn.cursor()

    try:

        cur.execute(
            'Select * from USERS where users_email = {}'.format(data['email']))
        
        if User.query.filter_by(user_email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        if not is_valid_password(data['password']):
            return jsonify({'error': 'Password not strong enough'}), 400

        # Hash the password
        hashed_password = generate_password_hash(
            data['password'], method='pbkdf2:sha256')
        new_user = User(
            user_name=data['username'],
            user_email=data['email'],
            # Using .get() allows for optional fields
            user_skin_type=data.get('skin_type', 'Default'),
            user_gender=data.get('gender', 'Prefer not to say'),
            hashed_password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return jsonify(new_user.to_dict()), 201

    except Exception as e:
        import traceback
        traceback.print_exc()  # This prints the full stack trace
        return jsonify({'error': 'Unexpected registration error'}), 500


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


def is_valid_password(password):
    """Checks basic password requirements"""
    if len(password) < 8:  # Example: Minimum 8 characters
        return False
    # You can add more checks: uppercase, lowercase, numbers, symbols, etc.
    return True


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
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Ensure that required fields are present in the data
        if 'ssreminder_freq' not in data or 'ssreminder_time' not in data:
            return jsonify({'error': 'Missing data for reminder frequency or time'}), 400
        data = request.get_json()
        new_reminder = SSReminder(user_id=user_id, **data)
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify(new_reminder.to_dict()), 201


@app.route('/users/<int:user_id>/sunscreen-reminders/<int:ssreminder_id>', methods=['PUT'])
def update_sunscreen_reminder(user_id, ssreminder_id):
    user = User.query.get_or_404(user_id)
    reminder = SSReminder.query.get_or_404(ssreminder_id)

    if reminder.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 401  # Authorization check

    data = request.get_json()
    for key, value in data.items():
        setattr(reminder, key, value)
    db.session.commit()
    return jsonify(reminder.to_dict())


@app.route('/users/<int:user_id>/sunscreen-reminders/<int:ssreminder_id>', methods=['DELETE'])
def delete_sunscreen_reminder(user_id, ssreminder_id):
    user = User.query.get_or_404(user_id)
    reminder = SSReminder.query.get_or_404(ssreminder_id)

    if reminder.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 401  # Authorization check

    db.session.delete(reminder)
    db.session.commit()
    return '', 204


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
        result['temp_alerts'] = [alert.to_dict()
                                 for alert in location.temp_alerts]

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
        query = query.filter(Mortality.location_lat.between(
            location_lat - 0.1, location_lat + 0.1))
        query = query.filter(Mortality.location_long.between(
            location_long - 0.1, location_long + 0.1))
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
        query = query.filter(Incidence.location_lat.between(
            location_lat - 0.1, location_lat + 0.1))
        query = query.filter(Incidence.location_long.between(
            location_long - 0.1, location_long + 0.1))
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
    latest_uv_record = UVRecord.query.filter_by(location_id=location_id).order_by(
        UVRecord.uvrecord_timestamp.desc()).first()
    latest_temp_alert = TempAlert.query.filter_by(location_id=location_id).order_by(
        TempAlert.temp_alert_timestamp.desc()).first()
    latest_uv_record = UVRecord.query.filter_by(location_id=location_id).order_by(
        UVRecord.uvrecord_timestamp.desc()).first()

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


@app.route('/clothing-recommendations', methods=['POST'])
def get_clothing_recommendations():
    data = request.get_json()
    uv_index = data.get('uv_index', 7)

    recommendations = []
    if uv_index >= 3:
        recommendations.append(
            {'clothing_type': 'Wide-brimmed hat', 'upf': 50})
        recommendations.append({'clothing_type': 'Sunglasses', 'upf': 400})

        if uv_index >= 6:
            # Recommend stronger protection
            recommendations.append({'clothing_type': 'Sunscreen', 'spf': 50})
            recommendations.append(
                {'clothing_type': 'UV-blocking umbrella', 'upf': 50})

            if uv_index >= 8:
                # Advise extra precautions
                recommendations.append(
                    {'clothing_type': 'UV-protective lip balm', 'spf': 30})
                recommendations.append(
                    {'clothing_type': 'Sun protective gloves', 'upf': 50})

                if uv_index >= 11:
                    # Suggest minimizing outdoor activities
                    recommendations.append(
                        {'clothing_type': 'Stay indoors or seek shade', 'note': 'UV index is extremely high'})

    print(data)
    return jsonify(recommendations)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5000)
