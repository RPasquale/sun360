from flask_sqlalchemy import SQLAlchemy
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.BigInteger, primary_key=True)
    user_name = db.Column(db.String(100), nullable=True)
    user_gender = db.Column(db.String(1), nullable=True)
    user_email = db.Column(db.String(100), unique=True, nullable=True)
    users_password = db.Column(db.String(255), nullable=True)  # Use users_password
    user_skin_type = db.Column(db.SmallInteger, nullable=True)
    suburb_id = db.Column(db.BigInteger, db.ForeignKey('suburb.suburb_id'), nullable=True)
    
    # Define relationships
    ss_reminders = db.relationship('SSReminder', back_populates='user', lazy=True)

    __table_args__ = (
        db.CheckConstraint("user_gender  IN ('M', 'F', 'X')", name='users_gender_chk'),
    )
            
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'user_skin_type': self.user_skin_type,
            'user_gender': self.user_gender,
            'ss_reminders': self.ss_reminders,
            'suburb_id': self.suburb_id
    
        }



class FamilyMember(db.Model):
    __tablename__ = 'family_member'
    fm_id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    fm_name = db.Column(db.String(100), nullable=True)
    fm_gender = db.Column(db.String(1), nullable=True)
    fm_skin_type = db.Column(db.SmallInteger, nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref='family_members')

    __table_args__ = (
        db.CheckConstraint("fm_gender IN ('M', 'F', 'X')", name='fm_gender_chk'),
    )

    def to_dict(self):
        return {
            'fm_id': self.fm_id,
            'fm_name': self.fm_name,
            'fm_gender': self.fm_gender,
            'fm_skin_type': self.fm_skin_type,
            'users_id': self.users_id
        }


class Suburb(db.Model):
    __tablename__ = 'suburb'
    suburb_id = db.Column(db.BigInteger, primary_key=True)  # assuming INT8 maps to BigInteger
    suburb_name = db.Column(db.String(100), nullable=True)
    suburb_postcode = db.Column(db.String(4), nullable=True)
    suburb_state = db.Column(db.String(50), nullable=True)
    suburb_lat = db.Column(db.Numeric, nullable=True)  # Using Numeric for DECIMAL
    suburb_long = db.Column(db.Numeric, nullable=True)

    users = db.relationship('User', backref='suburb', lazy=True)

    def to_dict(self):
        return {
            'suburb_id': self.suburb_id,
            'suburb_name': self.suburb_name,
            'suburb_postcode': self.suburb_postcode,
            'suburb_state': self.suburb_state,
            'suburb_lat': self.suburb_lat,
            'suburb_long': self.suburb_long,
            'users': self.users
        }


class SSReminder(db.Model):
    __tablename__ = 'ssreminder'
    ssreminder_id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)  # Assuming INT8 maps to BigInteger
    ssreminder_type = db.Column(db.String(1), nullable=True)
    ssreminder_date = db.Column(db.Date, nullable=True)
    ssreminder_time = db.Column(db.Time, nullable=True)
    ssreminder_weekday = db.Column(db.String(2), nullable=True)
    ssreminder_title = db.Column(db.String(100), nullable=True)
    ssreminder_notes = db.Column(db.Text, nullable=True)  # Using Text for STRING
    ssreminder_color_code = db.Column(db.String(1), nullable=True)
    ssreminder_status = db.Column(db.String(1), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref='ss_reminders')  

    # Define relationships
    user = db.relationship('User', back_populates='ss_reminders')

    __table_args__ = (
        db.CheckConstraint("ssreminder_type IN ('O', 'D', 'W')", name='ssreminder_type_chk'),
        db.CheckConstraint("ssreminder_weekday IN ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')", name='ssreminder_weekday_chk'),
        db.CheckConstraint("ssreminder_color_code IN ('R', 'Y', 'G')", name='ssreminder_color_code_chk'),
        db.CheckConstraint("ssreminder_status IN ('P', 'C', 'U')", name='ssreminder_status_chk'),
    )

    def to_dict(self):
        return {
            'ssreminder_id': self.ssreminder_id,
            'ssreminder_type': self.ssreminder_type,
            'ssreminder_date': self.ssreminder_date.strftime('%Y-%m-%d') if self.ssreminder_date else None,
            'ssreminder_time': self.ssreminder_time.strftime('%H:%M:%S') if self.ssreminder_time else None,
            'ssreminder_weekday': self.ssreminder_weekday,
            'ssreminder_title': self.ssreminder_title,
            'ssreminder_notes': self.ssreminder_notes,
            'ssreminder_color_code': self.ssreminder_color_code,
            'ssreminder_status': self.ssreminder_status,
            'users_id': self.users_id
        }                     

 
class CancerStatistics(db.Model):
    __tablename__ = 'cancer_statistics'
    rowid = db.Column(db.BigInteger, primary_key=True)
    cancer_group = db.Column(db.String(100), nullable=True)
    cancer_year = db.Column(db.BigInteger, nullable=True)
    cancer_gender = db.Column(db.String(1), nullable=True)
    cancer_age_group = db.Column(db.String(20), nullable=True)
    cancer_incidence_count = db.Column(db.BigInteger, nullable=True)
    cancer_age_specific_incidence_rate = db.Column(db.Numeric, nullable=True)
    cancer_mortality_count = db.Column(db.BigInteger, nullable=True)
    cancer_age_specific_mortality_rate = db.Column(db.Numeric, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('cancer_group', 'cancer_year', 'cancer_gender', 'cancer_age_group', name='cancer_statistics_unq'),
        db.CheckConstraint("cancer_gender IN ('M', 'F')", name='cancer_statistics_chk'),
    )

    def to_dict(self):
        return {
            'rowid': self.rowid,
            'cancer_group': self.cancer_group,
            'cancer_year': self.cancer_year,
            'cancer_gender': self.cancer_gender,
            'cancer_age_group': self.cancer_age_group,
            'cancer_incidence_count': self.cancer_incidence_count,
            'cancer_age_specific_incidence_rate': str(self.cancer_age_specific_incidence_rate),
            'cancer_mortality_count': self.cancer_mortality_count,
            'cancer_age_specific_mortality_rate': str(self.cancer_age_specific_mortality_rate),
        }


class CancerIncidence(db.Model):
    __tablename__ = 'cancer_incidence'
    rowid = db.Column(db.BigInteger, primary_key=True)
    cancer_group = db.Column(db.String(100), nullable=True)
    cancer_year = db.Column(db.BigInteger, nullable=True)
    cancer_gender = db.Column(db.String(1), nullable=True)
    cancer_state = db.Column(db.String(50), nullable=True)
    cancer_incidence_count = db.Column(db.BigInteger, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('cancer_group', 'cancer_year', 'cancer_gender', 'cancer_state', name='cancer_incidence_unq'),
        db.CheckConstraint("cancer_gender IN ('M', 'F')", name='cancer_gender_chk'),
        db.CheckConstraint("cancer_state IN ('ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA')", name='cancer_state_chk'),
    )

    def to_dict(self):
        return {
            'rowid': self.rowid,
            'cancer_group': self.cancer_group,
            'cancer_year': self.cancer_year,
            'cancer_gender': self.cancer_gender,
            'cancer_state': self.cancer_state,
            'cancer_incidence_count': self.cancer_incidence_count,
        }


