from flask import Flask, jsonify, request
from models import User, FamilyMember, Suburb,SSReminder, CancerStatistics,  CancerIncidence 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from faker import Faker 
from flask_cors import CORS
from config import Config
import os  # For environment variables 
from dotenv import load_dotenv
from extensions import db, login_manager
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector

load_dotenv() 
print(os.environ.get("DATABASE_URL"))

#######################################################
# Real Data
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
CORS(app)


# Add this command to your app.py
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
#########################################################
# USERS, Login, Register, Logout
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')  # Use email to match users_email
    password = data.get('password')

    user = User.query.filter_by(users_email=email).first()

    if user and check_password_hash(user.users_password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

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
        if User.query.filter_by(user_email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        if not is_valid_password(data['password']):
            return jsonify({'error': 'Password not strong enough'}), 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        
        # Correctly referencing the 'suburb_name' attribute in the Suburb model
        suburb = Suburb.query.filter_by(suburb_name=data.get('suburb_name')).first()
        
        if suburb is None:
            # Creating a new Suburb instance with the correct attribute
            suburb = Suburb(suburb_name=data.get('suburb_name'))
            db.session.add(suburb)
            db.session.commit()

        new_user = User(
            user_name=data.get('username'),
            user_email=data['email'],
            user_skin_type=data.get('skin_type', 2),
            user_gender=data.get('gender', 'X'),
            users_password=hashed_password,
            suburb_id=suburb.suburb_id
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return jsonify(new_user.to_dict()), 201

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the full stack trace for debugging
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
#########################################################
# LOCATIONS
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
        result['suburbs'] = [suburb.to_dict() for suburb in suburb_name.suburbs]
    # Add similar logic for other related data (temp_alerts, uv_records) as required

    return jsonify(result) 

#########################################################
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
#########################################################
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


