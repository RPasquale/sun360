from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_skin_type = db.Column(db.String(50), nullable=False) 
    user_gender = db.Column(db.String(20), nullable=False)  

    ss_applications = db.relationship('SSAppl', backref='user', lazy=True)
    ss_reminders = db.relationship('SSReminder', backref='user', lazy=True)



class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(80), nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)

    # Relationships
    temp_alerts = db.relationship('TempAlert', backref='location', lazy=True)
    suburbs = db.relationship('Suburb', backref='location', lazy=True)
    uv_records = db.relationship('UVRecord', backref='location', lazy=True)
    users = db.relationship('User', backref='location', lazy=True)


class TempAlert(db.Model):
    temp_alert_id = db.Column(db.Integer, primary_key=True)
    temp_alert_timestamp = db.Column(db.DateTime, nullable=False)
    temp_alert_desc = db.Column(db.String(250), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)

class Suburb(db.Model):
    suburb_id = db.Column(db.Integer, primary_key=True) 
    suburb_name = db.Column(db.String(80), nullable=False)
    suburb_postcode = db.Column(db.Integer, nullable=False) 
    suburb_state = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    suburb_lat = db.Column(db.Float, nullable=False)
    suburb_long = db.Column(db.Float, nullable=False)



class UVRecord(db.Model):
    uvrecord_timestamp = db.Column(db.DateTime, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    uvindex_value = db.Column(db.Float, nullable=False)
    temp_value = db.Column(db.Float, nullable=False)

    ss_applications = db.relationship('SSAppl', backref='uv_record', lazy=True)


class Clothing(db.Model):
    clothing_id = db.Column(db.Integer, primary_key=True)
    clothing_type = db.Column(db.String(80), nullable=False)
    clothing_upf = db.Column(db.Integer, nullable=False) 


class SSAppl(db.Model): 
    ssappl_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    uvindex_id = db.Column(db.DateTime, db.ForeignKey('uvrecord.uvrecord_timestamp'), nullable=False) 
    ssappl_amount = db.Column(db.String(50), nullable=False) 
    ssappl_timestamp = db.Column(db.DateTime, nullable=False)


class SSReminder(db.Model):
    ssreminder_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ssreminder_freq = db.Column(db.String(50), nullable=False) 
    ssreminder_time = db.Column(db.Time, nullable=False) 
    ssreminder_message = db.Column(db.String(250), nullable=False)
    ssreminder_status = db.Column(db.String(20), nullable=False) 


class Mortality(db.Model):
    morti_id = db.Column(db.Integer, primary_key=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)
    cancer_type = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mort_count = db.Column(db.Integer, nullable=False) 
    mortil_age_group = db.Column(db.String(80), nullable=False)
    mortil_sex = db.Column(db.String(20), nullable=False)


class Incidence(db.Model):
    inci_id = db.Column(db.Integer, primary_key=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)
    cancer_type = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    inci_count = db.Column(db.Integer, nullable=False) 
    inci_age_group = db.Column(db.String(80), nullable=False)
    inci_sex = db.Column(db.String(20), nullable=False) 

