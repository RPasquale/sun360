from flask import Flask, jsonify, request
from models import Users, FamilyMember, Suburb, Suburb_Shp, SSReminder, CancerStatistics,  CancerIncidence
import secrets
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import os  # For environment variables
from dotenv import load_dotenv
from extensions import db
from flask import Flask
from sqlalchemy import create_engine, func, and_
from sqlalchemy.engine.reflection import Inspector

# AI Model Libraries
from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForImageClassification, AutoFeatureExtractor
from PIL import Image
import io
import os
import json
from torchvision import transforms

load_dotenv()

#######################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
owapi_base_url = 'https://api.openweathermap.org/data/2.5/onecall?lat=<<lat>>&lon=<<lon>>&exclude=hourly,daily,minutely,alerts&appid=' + \
    os.environ.get('OPEN_WEATHER_API_KEY')
db.init_app(app)
CORS(app, supports_credentials=True, allow_headers="*", origins="*")

# # Constants and model paths
# model_path = os.getcwd() + '\\sun360\\ai_models\\fine_tuned_model'
# print(model_path)
# print("Does the directory exist?", os.path.isdir(model_path))
# print("Does config.json exist?", os.path.isfile(
#     os.path.join(model_path, 'config.json')))

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Load the pre-trained model
# model = AutoModelForImageClassification.from_pretrained(model_path).to(device)
# model.eval()

# # Load the feature extractor
# feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)

# # Load the label mappings
# label_to_id_path = os.path.join(model_path, 'label_to_id.json')
# id_to_label_path = os.path.join(model_path, 'id_to_label.json')

# with open(label_to_id_path, 'r') as file:
#     label_to_id = json.load(file)

# with open(id_to_label_path, 'r') as file:
#     id_to_label = json.load(file)

# # Define the data preprocessing transformations
# data_transforms = transforms.Compose([
#     transforms.Resize(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])


@app.cli.command("check-tables")
def check_tables():
    """Check if tables exist in the database."""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = Inspector.from_engine(engine)
    tables = inspector.get_table_names()
    if tables:
        print("Found tables in the database:")
        for table in tables:
            print(f"- {table}")
    else:
        print("No tables found in the database.")


@app.cli.command("create-db")
def create_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()

#######################################################
# Basic Routes (Placeholders )


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Sun360 API!'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

########################################################
# Middlewares


def check_header():
    # Check if the 'Authorization' header is present
    if 'Authorization' not in request.headers:
        return jsonify({'error': 'Missing Authorization header'}), 401

    if 'Access-ID' not in request.headers:
        return jsonify({'error': 'Missing Access-ID header'}), 401

    authorization = request.headers.get('Authorization')
    access_id = int(request.headers.get('Access-ID'))

    user = Users.query.filter_by(users_id=access_id).first()
    if not user:
        return jsonify({'error': 'Invalid Access ID'}), 401

    if user.users_access_token != authorization:
        return jsonify({'error': 'Invalid Authorization'}), 401

    return None

# Apply the middleware to specific routes


@app.before_request
def protect_route():
    # Only apply the middleware to specific routes
    # List the endpoints where you want to apply the middleware
    if request.endpoint in ['logout']:
        return check_header()


#########################################################
# USERS, Login, Register, Logout

def login_user(user):
    try:
        access_token = secrets.token_hex(32)
        Users.query.filter_by(users_id=user.users_id).update(
            {"users_access_token": access_token})
        db.session.commit()
        return access_token
    except:
        return None


def logout_user(users_id):
    try:
        Users.query.filter_by(users_id=users_id).update(
            {"users_access_token": None})
        db.session.commit()
        return True
    except:
        return False


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('users_email')  # Use email to match users_email
    password = data.get('users_password')

    user = Users.query.filter_by(users_email=email).first()
    if user and check_password_hash(user.users_password, password):
        access_token = login_user(user)
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'access_id': '{}'.format(user.users_id)}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    users_id = request.headers.get('Access-ID')
    if logout_user(users_id):
        return jsonify({'message': 'Logged out'}), 200
    else:
        return jsonify({'error': 'Unable to logout'}), 401


def is_valid_password(password):
    """Checks basic password requirements"""
    if len(password) < 8:  # Example: Minimum 8 characters
        return False
    # You can add more checks: uppercase, lowercase, numbers, symbols, etc.
    return True


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    try:

        if Users.query.filter_by(users_email=data.get('users_email')).first():
            return jsonify({'error': 'Email already exists'}), 400

        if not is_valid_password(data.get('users_password')):
            return jsonify({'error': 'Password not strong enough'}), 400

        hashed_password = generate_password_hash(
            data.get('users_password'), method='pbkdf2:sha256')

        # Correctly referencing the 'suburb_name' attribute in the Suburb model
        suburb = Suburb.query.filter(and_(
            func.lower(Suburb.suburb_name) == data.get('suburb_name').lower(),
            Suburb.suburb_postcode == data.get('suburb_postcode')
        )).first()

        if suburb is None:
            # Creating a new Suburb instance with the correct attribute
            suburb = Suburb(suburb_name=data.get('suburb_name'),
                            suburb_postcode=data.get('suburb_postcode'))
            db.session.add(suburb)
            db.session.commit()

        new_user = Users(
            users_name=data.get('users_name'),
            users_email=data.get('users_email'),
            users_password=hashed_password,
            users_age=data.get('users_age'),
            users_skin_type=data.get('users_skin_type', 2),
            users_gender=data.get('users_gender', 'X'),
            users_access_token=None,
            suburb_id=suburb.suburb_id)

        db.session.add(new_user)
        db.session.commit()

        # Get updated user for getting the autogenerated ID
        new_user = Users.query.filter_by(
            users_email=data.get('users_email')).first()

        family_members = data.get('users_family_members')
        if (family_members and len(family_members) > 0):
            for fm_idx in range(len(family_members)):
                data_fm = family_members[fm_idx]
                new_family_member = FamilyMember(fm_name=data_fm.get('fm_name'),
                                                 fm_gender=data_fm.get(
                                                     'fm_gender'),
                                                 fm_age=data_fm.get('fm_age'),
                                                 fm_skin_type=data_fm.get(
                                                     'fm_skin_type'),
                                                 users_id=new_user.users_id
                                                 )
                db.session.add(new_family_member)
                db.session.commit()

        return jsonify(new_user.to_dict()), 201

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the full stack trace for debugging
        return jsonify({'error': 'Unexpected registration error'}), 500


@app.route('/users/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(users_id):
    user = Users.query.get_or_404(users_id)

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

#########################################################
# LOCATIONS


@app.route('/suburb-UV-temp', methods=['GET'])
def get_data_for_suburbs():
    # All Shape File locations
    all_suburbs = Suburb_Shp.query.all()
    for suburb in all_suburbs[:1]:
        lat = suburb.suburb_shp_lat
        lon = suburb.suburb_shp_long
        owapi_url = owapi_base_url.replace(
            '<<lat>>', str(lat)).replace('<<lon>>', str(lon))
        print(owapi_url)
        response = requests.get(owapi_url)
        print(response.json())
    return jsonify(all_suburbs)


@app.route('/locations', methods=['GET'])
def get_locations():
    all_locations = Suburb.query.all()
    result = [loc.to_dict() for loc in all_locations]
    return jsonify(result)


@app.route('/locations/<int:location_id>', methods=['GET'])
def get_location(suburb_name):
    location = Suburb.query.get_or_404(suburb_name)

    # Include related data if needed
    result = suburb_name.to_dict()
    if request.args.get('include_suburbs'):
        result['suburbs'] = [suburb.to_dict()
                             for suburb in suburb_name.suburbs]
    # Add similar logic for other related data (temp_alerts, uv_records) as required

    return jsonify(result)

#########################################################
# SUNSCREEN REMINDERS


@app.route('/users/<int:users_id>/sunscreen-reminders', methods=['GET', 'POST'])
def manage_sunscreen_reminders(users_id):
    # Check if the user exists
    user = Users.query.get_or_404(users_id)
    if not user:
        return jsonify({'error': 'Invalid User'}), 400

    if request.method == 'GET':
        reminders = user.ss_reminders  # Fetch reminders via relationship
        result = [reminder.to_dict() for reminder in reminders]
        return jsonify(result)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        ssreminder_type = data.get('ssreminder_type')

        # Ensure that required fields are present in the data
        if ssreminder_type == 'O' and (('ssreminder_date' not in data) or ('ssreminder_time' not in data)):
            return jsonify({'error': 'Missing data for reminder date or time'}), 400

        if ssreminder_type == 'D' and ('ssreminder_time' not in data):
            return jsonify({'error': 'Missing data for reminder time'}), 400

        if ssreminder_type == 'W' and ('ssreminder_weekday' not in data or 'ssreminder_time' not in data):
            return jsonify({'error': 'Missing data for reminder weekdays or time'}), 400

        if 'ssreminder_title' not in data:
            return jsonify({'error': 'Missing data for reminder title'}), 400

        new_reminder = SSReminder(users_id=users_id,
                                  ssreminder_type=data.get('ssreminder_type'),
                                  ssreminder_date=data.get('ssreminder_date'),
                                  ssreminder_time=data.get('ssreminder_time'),
                                  ssreminder_weekday=data.get(
                                      'ssreminder_weekday'),
                                  ssreminder_title=data.get(
                                      'ssreminder_title'),
                                  ssreminder_notes=data.get(
                                      'ssreminder_notes') or '',
                                  ssreminder_color_code=data.get(
                                      'ssreminder_color_code') or 'Y',
                                  ssreminder_status='P')
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify(new_reminder.to_dict()), 201


@app.route('/users/<int:users_id>/sunscreen-reminders/<int:ssreminder_id>', methods=['PUT'])
def update_sunscreen_reminder(users_id, ssreminder_id):
    user = Users.query.get_or_404(users_id)
    reminder = SSReminder.query.get_or_404(ssreminder_id)

    if reminder.users_id != users_id:
        return jsonify({'error': 'Unauthorized'}), 401  # Authorization check

    data = request.get_json()
    for key, value in data.items():
        setattr(reminder, key, value)
    db.session.commit()
    return jsonify(reminder.to_dict())


@app.route('/users/<int:users_id>/sunscreen-reminders/<int:ssreminder_id>', methods=['DELETE'])
def delete_sunscreen_reminder(users_id, ssreminder_id):
    user = Users.query.get_or_404(users_id)
    reminder = SSReminder.query.get_or_404(ssreminder_id)

    if reminder.users_id != users_id:
        return jsonify({'error': 'Unauthorized'}), 401  # Authorization check

    db.session.delete(reminder)
    db.session.commit()
    return '', 204


#########################################################

# Skin Spot Prediction routes

@app.route('/predict_image', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image_bytes = file.read()

    try:
        # Preprocess the image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        inputs = feature_extractor(
            images=image, return_tensors="pt") if feature_extractor else data_transforms(image).unsqueeze(0)
        pixel_values = inputs['pixel_values'].to(
            device) if feature_extractor else inputs.to(device)

        # Make prediction
        with torch.no_grad():
            outputs = model(pixel_values)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)
        predicted_label = id_to_label[str(predictions.item())]

        return jsonify({'prediction': predicted_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''# UV DATA (Simplified)
@app.route('/uv-data', methods=['GET'])
def get_uv_data():
    # Example: Get all UV records 
    uv_records = UVRecord.query.all()
    result = [record.to_dict() for record in uv_records]
    return jsonify(result) 

#########################################################
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
#########################################################
# Suburbs
@app.route('/locations/<int:location_id>/suburbs', methods=['GET'])
def get_suburbs_for_location(location_id):
    location = Location.query.get_or_404(location_id)  # Get the location
    suburbs = location.suburbs  # Fetch related suburbs via the relationship
    result = [suburb.to_dict() for suburb in suburbs]
    return jsonify(result)
#########################################################
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
#########################################################
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
#########################################################

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
        recommendations.append({'clothing_type': 'Wide-brimmed hat', 'upf': 50})
        recommendations.append({'clothing_type': 'Sunglasses', 'upf': 400})
        
        if uv_index >= 6:
            # Recommend stronger protection
            recommendations.append({'clothing_type': 'Sunscreen', 'spf': 50})
            recommendations.append({'clothing_type': 'UV-blocking umbrella', 'upf': 50})

            if uv_index >= 8:
                # Advise extra precautions
                recommendations.append({'clothing_type': 'UV-protective lip balm', 'spf': 30})
                recommendations.append({'clothing_type': 'Sun protective gloves', 'upf': 50})

                if uv_index >= 11:
                    # Suggest minimizing outdoor activities
                    recommendations.append({'clothing_type': 'Stay indoors or seek shade', 'note': 'UV index is extremely high'})

    print(data)
    return jsonify(recommendations)
'''


########################################################################
'''# AI Model Routes
import io 
import torch
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image
from datasets import load_dataset  
import numpy as np
from transformers import AutoModelForImageClassification, AutoFeatureExtractor, TrainingArguments, Trainer

# Constants and model names
model_name = r"D:\sun360\ai_models\fine_tuned_model"
print("Does the directory exist?", os.path.isdir(model_name))
print("Does config.json exist?", os.path.isfile(os.path.join(model_name, 'config.json')))


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the pre-trained model
model = AutoModelForImageClassification.from_pretrained(model_name).to(device)
model.eval()

# Feature extractor for preprocessing images
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)

# Data preprocessing transformations (assuming consistency with training)
data_transforms = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
dataset_path = "marmal88/skin_cancer"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the dataset from Hugging Face
dataset = load_dataset(dataset_path)
unique_labels = set()
for example in dataset['train']:
    unique_labels.add(example['dx'])
unique_labels = sorted(list(unique_labels))
label_to_id = {label: id for id, label in enumerate(unique_labels)}
id_to_label = {id: label for label, id in label_to_id.items()}


@app.route('/predict_image', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image_bytes = file.read()

    try:
        # Preprocess the image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        inputs = feature_extractor(images=image, return_tensors="pt") if feature_extractor else data_transforms(image).unsqueeze(0)
        pixel_values = inputs['pixel_values'].to(device) if feature_extractor else inputs.to(device)

        # Make prediction
        with torch.no_grad():
            outputs = model(pixel_values)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)
        predicted_label = id_to_label[predictions.item()]

        return jsonify({'prediction': predicted_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
########################################################################

# Real Database:
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()  # Attempt to create the database tables
            print("Database tables created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the database tables: {e}")
    app.run(debug=True, port=5000)
