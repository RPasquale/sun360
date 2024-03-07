from models import *
import psycopg2

# RUN IN POWERSHELL FOR DOWNLOADING CERTIFICATE FOR RUNNING COCKROACHDB
# mkdir -p $env:appdata\postgresql\; Invoke-WebRequest -Uri https://cockroachlabs.cloud/clusters/18ab3bdc-c5c5-429e-8600-e58a9c89fef7/cert -OutFile $env:appdata\postgresql\root.crt

conn = psycopg2.connect(
    "postgresql://ta11:Ma5sm0_QVsBHDEVrk0LJuw@sun360-1974.g8x.gcp-southamerica-east1.cockroachlabs.cloud:26257/sun360?sslmode=verify-full")

with conn.cursor() as cur:
    # Creation of Table schemas
    # # Suburb Table
    # cur.execute("""CREATE TABLE IF NOT EXISTS SUBURB (
    #     suburb_id SERIAL PRIMARY KEY,
    #     suburb_name VARCHAR(100),
    #     suburb_postcode VARCHAR(4),
    #     suburb_state VARCHAR(50),
    #     suburb_lat DECIMAL,
    #     suburb_long DECIMAL
    # );""")

    # # User Table
    # cur.execute("""CREATE TABLE IF NOT EXISTS USERS (
    #     users_id SERIAL PRIMARY KEY,
    #     users_name VARCHAR(100),
    #     users_gender CHAR(1),
    #     users_email VARCHAR(100),
    #     users_password VARCHAR(255),
    #     users_skin_type SMALLINT,
    #     suburb_id INTEGER
    # );""")

    # cur.execute(
    #     """ALTER TABLE USERS ADD CONSTRAINT users_email_unique UNIQUE ( users_email )""")
    # cur.execute(
    #     """ALTER TABLE USERS ADD CONSTRAINT users_gender_chk CHECK ( users_gender IN ( 'M', 'F', 'X' ))""")
    # cur.execute(
    #     """ALTER TABLE USERS ADD CONSTRAINT users_suburb FOREIGN KEY ( suburb_id ) REFERENCES SUBURB ( suburb_id );""")

    # # Family Member Table
    # cur.execute("""CREATE TABLE IF NOT EXISTS FAMILY_MEMBER (
    #     fm_id SERIAL PRIMARY KEY,
    #     fm_name VARCHAR(100),
    #     fm_gender CHAR(1),
    #     fm_skin_type SMALLINT,
    #     users_id INTEGER
    # );""")

    # cur.execute(
    #     """ALTER TABLE FAMILY_MEMBER ADD CONSTRAINT fm_gender_chk CHECK ( fm_gender IN ( 'M', 'F', 'X' ));""")
    # cur.execute("""ALTER TABLE FAMILY_MEMBER ADD CONSTRAINT users_family_member FOREIGN KEY ( users_id ) REFERENCES  USERS ( users_id );""")

    # # Reminders Table
    # cur.execute("""CREATE TABLE IF NOT EXISTS SSREMINDER (
    #     ssreminder_id SERIAL PRIMARY KEY,
    #     ssreminder_type VARCHAR(1),
    #     ssreminder_date DATE,
    #     ssreminder_time TIME,
    #     ssreminder_weekday VARCHAR(2),
    #     ssreminder_title VARCHAR(100),
    #     ssreminder_notes TEXT,
    #     ssreminder_color_code VARCHAR(1),
    #     ssreminder_status VARCHAR(1),
    #     users_id INTEGER
    # );""")

    # # Comments related to codes and short forms
    # cur.execute("""COMMENT ON COLUMN SSREMINDER.ssreminder_type IS 'Type of reminders based on frequency, O: One Time, D: Daily, W: Weekly'""")
    # cur.execute(
    #     """COMMENT ON COLUMN SSREMINDER.ssreminder_weekday IS 'Weekday for weekly reminders, MO, TU, WE, TH, FR, SA, SU'""")
    # cur.execute(
    #     """COMMENT ON COLUMN SSREMINDER.ssreminder_color_code IS 'User set severity of reminders, R: Red, Y: Yellow, G: Green'""")
    # cur.execute(
    #     """COMMENT ON COLUMN SSREMINDER.ssreminder_status IS 'Status of reminder, P: Pending, C: Completed, U: Unprotected'""")

    # cur.execute(
    #     """ALTER TABLE SSREMINDER ADD CONSTRAINT ssreminder_type_chk CHECK ( ssreminder_type IN ( 'O', 'D', 'W' ));""")
    # cur.execute(
    #     """ALTER TABLE SSREMINDER ADD CONSTRAINT ssreminder_weekday_chk CHECK ( ssreminder_weekday IN ( 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'));""")
    # cur.execute(
    #     """ALTER TABLE SSREMINDER ADD CONSTRAINT ssreminder_color_code_chk CHECK ( ssreminder_color_code IN ( 'R', 'Y', 'G' ));""")
    # cur.execute(
    #     """ALTER TABLE SSREMINDER ADD CONSTRAINT ssreminder_status_chk CHECK ( ssreminder_status IN ( 'P', 'C', 'U' ));""")
    # cur.execute(
    #     """ALTER TABLE SSREMINDER ADD CONSTRAINT USERS_SSREMINDER FOREIGN KEY ( users_id ) REFERENCES  USERS ( users_id );""")

    # # Cancer Statistics Table
    # cur.execute("""CREATE TABLE IF NOT EXISTS CANCER_STATISTICS (
    #     cancer_group VARCHAR(100),
    #     cancer_year INTEGER,
    #     cancer_gender CHAR(1),
    #     cancer_age_group VARCHAR(20),
    #     cancer_incidence_count INTEGER,
    #     cancer_age_specific_incidence_rate DECIMAL,
    #     cancer_mortality_count INTEGER,
    #     cancer_age_specific_mortality_rate DECIMAL);""")
    
    # cur.execute("""ALTER TABLE CANCER_STATISTICS ADD CONSTRAINT CANCER_STATISTICS_CHK CHECK (cancer_gender in ('M','F'))""")

    # # Cancer Incidence Table
    # cur.execute("""CREATE TABLE IF NOT EXISTS CANCER_INCIDENCE (
    # cancer_group VARCHAR(100),
    # cancer_year INTEGER,
    # cancer_gender CHAR(1),
    # cancer_state VARCHAR(50),
    # cancer_incidence_count INTEGER);""")
    
    # cur.execute("""ALTER TABLE CANCER_INCIDENCE ADD CONSTRAINT CANCER_GENDER_CHK CHECK (cancer_gender in ('M', 'F'))""")
    # cur.execute("""ALTER TABLE CANCER_INCIDENCE ADD CONSTRAINT CANCER_STATE_CHK CHECK (cancer_state in ('ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'))""")
    # cur.execute("""ALTER TABLE CANCER_INCIDENCE ADD CONSTRAINT CANCER_INCIDENCE_UNQ UNIQUE (cancer_group, cancer_year, cancer_gender, cancer_state)""")
    
    # Insertion into Suburb Table (removed and saved elsewhere, really long)

    # Test insertion into Users Table
    # cur.execute("""INSERT INTO USERS (users_name, users_gender, users_email, users_password, users_skin_type, suburb_id)
    #             VALUES ('Lokesh', 'M', 'lkaggarwal1997@gmail.com', 'hfjsufusyfuxjkskirfucd', 2, 949126420277755905);""")

    # Test insertion into Family Members Table
    # cur.execute("""INSERT INTO FAMILY_MEMBER (fm_name, fm_gender, fm_skin_type, users_id)
    #             VALUES
    #             ('Lokesh Jr 1', 'M', 3, 949129620564049921),
    #             ('Lokesh Jr 2', 'F', 1, 949129620564049921);""")

    # Test insertion into SSReminder Table
    # cur.execute("""INSERT INTO SSREMINDER (ssreminder_type, ssreminder_date, ssreminder_time, ssreminder_weekday, ssreminder_title, ssreminder_notes, ssreminder_color_code, ssreminder_status)
    #             VALUES
    #             ('O', '2024-03-07', '13:00:00', 'MO', 'Playground', 'Add twice to Lokesh Jr 1', 'Y', 'P');""")

    conn.commit()
    conn.close()
