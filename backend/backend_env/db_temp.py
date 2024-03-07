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

# # cur.execute("""CREATE TABLE MORTALITY (
# #     mortl_id SERIAL PRIMARY KEY,
# #     mortl_cancer_type VARCHAR(100),
# #     mortl_year INTEGER,
# #     mortl_sex CHAR(1),
# #     mortl_age_group VARCHAR(20),
# #     mortl_count INTEGER
# # );""")


# # cur.execute(
# #     "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
# print(cur.execute("DROP TABLE test;"))
# # Pass data to fill a query placeholders and let Psycopg perform
# # the correct conversion (no more SQL injections!)
# # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# # # Query the database and obtain data as Python objects
# # cur.execute("SELECT * FROM test;")
# # print(cur.fetchone())


# # Make the changes to the database persistent
# conn.commit()
# conn.close()


# Connect to your SQLite3 cloud database
# conn = sqlite3.connect('sqlitecloud://admin:TA11sun360@nv9zosfaik.sqlite.cloud:8860\sun360.db')  # Replace 'path_to_your_database_file.db' with your database file path

# # Create a cursor object to interact with the database
# cursor = conn.cursor()

# # Define a function to create tables based on your model classes
# def create_tables():
#     # Iterate over each model class and create the corresponding table
#     for model_class in [YourModel1, YourModel2]:  # Add more model classes as needed
#         table_name = model_class.__tablename__
#         columns = ', '.join([f'{column_name} {column_type}' for column_name, column_type in model_class.__table__.items()])
#         create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})'
#         cursor.execute(create_table_query)

#     # Commit changes and close connection
#     conn.commit()
#     conn.close()

# # Call the function to create tables
# # create_tables()

# conn.close()


# up.uses_netloc.append("postgres")
# url = up.urlparse(os.environ.get("DATABASE_URL")
#                   or "postgres://emgxnsgc:EnycfxImNzGTrseE9G9P11Gqm2u3L_ZI@rain.db.elephantsql.com/emgxnsgc")


# conn = psycopg2.connect(database=url.path[1:],
#                         user=url.username,
#                         password=url.password,
#                         host=url.hostname,
#                         port=url.port
#                         )
