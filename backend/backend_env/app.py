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

@app.route('/locations/<int:location_id>', methods=['GET']) 
def get_location(location_id):
    location = Location.query.get_or_404(location_id)  # Fetch by ID or return 404
    return jsonify(location.to_dict()) 



@app.route('/users/<int:user_id>/sunscreen-reminders', methods=['POST'])
def create_sunscreen_reminder(user_id):
    # Handle reminder creation logic
    pass 



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
        # ... Logic to create a new reminder and associate it with the user
        pass  






# ... (other imports and app setup)

# LOCATIONS
@app.route('/locations', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()
    result = [loc.to_dict() for loc in all_locations]  
    return jsonify(result)

@app.route('/locations/<int:location_id>', methods=['GET']) 
def get_location(location_id):
    location = Location.query.get_or_404(location_id)  # Fetch by ID or return 404
    return jsonify(location.to_dict()) 











# Run the App (Development Mode)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables 
    app.run(debug=True) 
