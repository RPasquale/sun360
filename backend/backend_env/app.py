from flask import Flask, jsonify, request
from models import db, Location, User, UVRecord, TempAlert  # Import all your models
from flask_sqlalchemy import SQLAlchemy
import os  # For environment variables 

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')  # Load from environment variable
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Initialize SQLAlchemy

# Basic Routes (Placeholders )
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Sun360 API!'})

@app.route('/locations', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()
    result = [loc.to_dict() for loc in all_locations]  
    return jsonify(result)

@app.route('/users/<int:user_id>/sunscreen-reminders', methods=['POST'])
def create_sunscreen_reminder(user_id):
    # Handle reminder creation logic
    pass 

# LOCATIONS
@app.route('/locations', methods=['GET']) 
def get_locations():
    # ... Fetch locations (example in previous responses)
    pass

@app.route('/locations/<int:location_id>', methods=['GET']) 
def get_location(location_id):
    # ... Fetch a single location by ID
    pass 

# USERS
@app.route('/users', methods=['POST']) 
def create_user():
    # ... Handle creating a new user 
    pass 

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id): 
    # ... Get a user, update a user, delete a user 
    pass 

# UV DATA
@app.route('/uv-data', methods=['GET'])
def get_uv_data():
    # ... Query UV records, potentially with filtering (date, location)
    pass 

# SUNSCREEN REMINDERS
@app.route('/users/<int:user_id>/sunscreen-reminders', methods=['GET', 'POST'])
def manage_sunscreen_reminders(user_id):
    # ...Get reminders for a user, create a new reminder   
    pass 



# Run the App (Development Mode)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables 
    app.run(debug=True) 
