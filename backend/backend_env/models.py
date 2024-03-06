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
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'user_skin_type': self.user_skin_type,
            'user_gender': self.user_gender,
            'ss_applications': self.ss_applications,
            'ss_reminders': self.ss_reminders
        }

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
        
    def to_dict(self):
        return {
            'location_id': self.location_id,
            'location_name': self.location_name,
            'location_lat': self.location_lat,
            'location_long': self.location_long,
            'temp_alerts': self.temp_alerts,
            'suburbs': self.suburbs,
            'uv_records': self.uv_records,
            'users': self.users
        }


class TempAlert(db.Model):
    temp_alert_id = db.Column(db.Integer, primary_key=True)
    temp_alert_timestamp = db.Column(db.DateTime, nullable=False)
    temp_alert_desc = db.Column(db.String(250), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)

    def to_dict(self):
        return {
            'temp_alert_id': self.temp_alert_id,
            'temp_alert_timestamp': self.temp_alert_timestamp,
            'temp_alert_desc': self.temp_alert_desc,
            'location_id': self.location_id
        }


class Suburb(db.Model):
    suburb_id = db.Column(db.Integer, primary_key=True) 
    suburb_name = db.Column(db.String(80), nullable=False)
    suburb_postcode = db.Column(db.Integer, nullable=False) 
    suburb_state = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    suburb_lat = db.Column(db.Float, nullable=False)
    suburb_long = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'suburb_id': self.suburb_id,
            'suburb_name': self.suburb_name,
            'suburb_postcode': self.suburb_postcode,
            'suburb_state': self.suburb_state,
            'location_id': self.location_id,
            'suburb_lat': self.suburb_lat,
            'suburb_long': self.suburb_long
        }


class UVRecord(db.Model):
    uvrecord_timestamp = db.Column(db.DateTime, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    uvindex_value = db.Column(db.Float, nullable=False)
    temp_value = db.Column(db.Float, nullable=False)
    ss_applications = db.relationship('SSAppl', backref='uv_record', lazy=True)

    def to_dict(self):
        return {
            'uvrecord_timestamp': self.uvrecord_timestamp,
            'location_id': self.location_id,
            'uvindex_value': self.uvindex_value,
            'ss_applications': self.ss_applications,
            'temp_value': self.temp_value
        }


class Clothing(db.Model):
    clothing_id = db.Column(db.Integer, primary_key=True)
    clothing_type = db.Column(db.String(80), nullable=False)
    clothing_upf = db.Column(db.Integer, nullable=False) 

    def to_dict(self):
        return {
            'clothing_id': self.clothing_id,
            'clothing_type': self.clothing_type,
            'clothing_upf': self.clothing_upf
        }


class SSAppl(db.Model): 
    ssappl_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    uvindex_id = db.Column(db.DateTime, db.ForeignKey('uvrecord.uvrecord_timestamp'), nullable=False) 
    ssappl_amount = db.Column(db.String(50), nullable=False) 
    ssappl_timestamp = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'ssappl_id': self.ssappl_id,
            'user_id': self.user_id,
            'uvindex_id': self.uvindex_id,
            'ssappl_amount': self.ssappl_amount,
            'ssappl_timestamp': self.ssappl_timestamp
        } 


class SSReminder(db.Model):
    ssreminder_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ssreminder_freq = db.Column(db.String(50), nullable=False) 
    ssreminder_time = db.Column(db.Time, nullable=False) 
    ssreminder_message = db.Column(db.String(250), nullable=False)
    ssreminder_status = db.Column(db.String(20), nullable=False)
    uv_index_threshold = db.Column(db.Integer, nullable=True)  # Make threshold optional
    temp_alert = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'ssreminder_id': self.ssreminder_id,
            'user_id': self.user_id,
            'ssreminder_freq': self.ssreminder_freq,
            'ssreminder_time': self.ssreminder_time,
            'ssreminder_message': self.ssreminder_message,
            'ssreminder_status': self.ssreminder_status,
            'uv_index_threshold': self.uv_index_threshold,
            'temp_alert': self.temp_alert
        } 


class Mortality(db.Model):
    morti_id = db.Column(db.Integer, primary_key=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)
    cancer_type = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mort_count = db.Column(db.Integer, nullable=False) 
    mortil_age_group = db.Column(db.String(80), nullable=False)
    mortil_sex = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'morti_id': self.morti_id,
            'location_lat': self.location_lat,
            'location_long': self.location_long,
            'cancer_type': self.cancer_type,
            'year': self.year,
            'mort_count': self.mort_count,
            'mortil_age_group': self.mortil_age_group,
            'mortil_sex': self.mortil_sex
        }


class Incidence(db.Model):
    inci_id = db.Column(db.Integer, primary_key=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)
    cancer_type = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    inci_count = db.Column(db.Integer, nullable=False) 
    inci_age_group = db.Column(db.String(80), nullable=False)
    inci_sex = db.Column(db.String(20), nullable=False) 

    
    def to_dict(self):
        return {
            'inci_id': self.inci_id,
            'location_lat': self.location_lat,
            'location_long': self.location_long,
            'cancer_type': self.cancer_type,
            'year': self.year,
            'inci_count': self.inci_count,
            'inci_age_group': self.inci_age_group,
            'inci_sex': self.inci_sex
        }


