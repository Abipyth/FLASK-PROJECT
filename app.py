from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import mysql.connector
import qrcode
import os

app = Flask(__name__)

app.secret_key = 'qrforbuses'
# Configure the upload folder (outside the static folder)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database connection setup
db_connection = mysql.connector.connect(
    host="",
    user="root",
    password="",
    database="qr_code"
)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        bus_depo_name = request.form.get("bus_depo_name")
        password = request.form.get("password")
        cursor = db_connection.cursor()

        # Retrieve admin data from the database
        select_query = "SELECT * FROM admin_login WHERE bus_depo_name = %s"
        cursor.execute(select_query, (bus_depo_name,))
        admin_data = cursor.fetchone()

        if admin_data and admin_data[2] == password:  # Index 2 is for password field
            session["logged_in"] = True
            session["bus_depo_name"] = bus_depo_name
            #return "Admin login successful!", "success"  # Flash success message
            cursor.close()
            return redirect(url_for("index"))

        cursor.close()
        return "Invalid credentials. Please try again.", "danger" # Flash error message

    # Render the admin_login.html template for GET requests
    return render_template("admin_login.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bus_number = request.form["bus_number"]
        from_place = request.form["from_place"]
        destination = request.form["destination"]
        num_of_stops = int(request.form["num_of_stops"])
        total_fare = request.form["total_fare"]  # Get the total fare entered by the admin
        message = request.form["message"]

        # Retrieve lists of stop names, bus fares, and bus timings
        stop_names = request.form.getlist("stop_name[]")
        stop_fares = request.form.getlist("stop_fare[]")
        stop_timings = request.form.getlist("stop_timing[]")

        # Insert bus information into the database
        cursor = db_connection.cursor()

        insert_query = "INSERT INTO bus_schedule (bus_number, from_place, destination, num_of_stops, total_fare, message) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (bus_number, from_place, destination, num_of_stops, total_fare,message)
        cursor.execute(insert_query, values)
        db_connection.commit()

        # Retrieve the ID of the inserted bus schedule
        bus_schedule_id = cursor.lastrowid

        # Insert stop information into the database
        for i in range(len(stop_names)):
            insert_stop_query = "INSERT INTO bus_stops (bus_schedule_id, stop_name, stop_fare, stop_timing) VALUES (%s, %s, %s, %s)"
            stop_values = (bus_schedule_id, stop_names[i], stop_fares[i], stop_timings[i])
            cursor.execute(insert_stop_query, stop_values)

        db_connection.commit()

        

  # Generate QR code with encoded details
        qr_data = f"Bus Number: {bus_number}\nFrom Place: {from_place}\nDestination: {destination}\nNumber of Stops: {num_of_stops}\nTotal Fare: {total_fare}\nMessage: {message}\n"

        for i in range(len(stop_names)):
            qr_data += f"Stop {i + 1}: {stop_names[i]}\nBus Fare: {stop_fares[i]}\nBus Timing: {stop_timings[i]}\n"


        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(f"static/{bus_number}.png")

        cursor.close()

        return redirect(url_for("success"))

    return render_template("index.html")

# Success route after adding a bus
@app.route("/success")
def success():
    cursor = db_connection.cursor()
    select_query = "SELECT * FROM bus_schedule ORDER BY id DESC LIMIT 1"
    cursor.execute(select_query)
    bus_data = cursor.fetchone()

    # Retrieve stop details for the specific bus route
    bus_schedule_id = bus_data[0]
    select_stops_query = "SELECT * FROM bus_stops WHERE bus_schedule_id = %s"
    cursor.execute(select_stops_query, (bus_schedule_id,))
    stop_details = cursor.fetchall()

    cursor.close()

    bus_number = bus_data[1]
    from_place = bus_data[2]
    destination = bus_data[3]
    num_of_stops = bus_data[4]
    total_fare = bus_data[5]
    message = bus_data[6] 

  

    return render_template("success.html", bus_number=bus_number, from_place=from_place,
                           destination=destination, num_of_stops=num_of_stops,
                           total_fare=total_fare, message=message, stops=stop_details)

@app.route("/insert_qr_code", methods=["GET", "POST"])
def insert_qr_code():
    qr_code_uploaded = False
    uploaded_qr_image = ""

    if request.method == "POST":
        bus_number = request.form.get("bus_number")
        qr_image = request.files["qr_image"]

        if qr_image and allowed_file(qr_image.filename):
            filename = secure_filename(qr_image.filename)
            qr_image_path = os.path.join("static", filename)
            qr_image.save(qr_image_path)

            # Save the QR code image data to the database
            cursor = db_connection.cursor()
            insert_query = "INSERT INTO qr_code_images (bus_number, image_path) VALUES (%s, %s)"
            cursor.execute(insert_query, (bus_number, qr_image_path))
            db_connection.commit()
            cursor.close()

            qr_code_uploaded = True
            uploaded_qr_image = qr_image_path

    return render_template("insert_qr_code.html", qr_code_uploaded=qr_code_uploaded)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/view_qr_codes")
def view_qr_codes():
    cursor = db_connection.cursor()
    select_query = "SELECT * FROM qr_code_images"
    cursor.execute(select_query)
    qr_codes = cursor.fetchall()
    cursor.close()

    print(qr_codes)  # Print the fetched data to the console

    return render_template("view_qr_codes.html", qr_codes=qr_codes)
from flask import redirect, url_for

@app.route('/filter')
def filter():
    return render_template('check_and_redirect.html')
from flask import send_from_directory


@app.route("/show_qr_code/<bus_numbers>")
def show_qr_code(bus_numbers):
    bus_numbers = bus_numbers.split(',')
    return render_template("show_qr_codes.html", bus_numbers=bus_numbers)

@app.route("/check_and_redirect", methods=["POST"])
def check_and_redirect():
    from_place = request.form["from_place"]
    destination = request.form["destination"]
    
    cursor = db_connection.cursor()
    select_query = "SELECT bus_number, from_place, destination FROM bus_schedule"
    cursor.execute(select_query)
    bus_schedule_entries = cursor.fetchall()
    cursor.close()

    matching_buses = []

    for entry in bus_schedule_entries:
        if entry[1] == from_place and entry[2] == destination:
            matching_buses.append(entry[0])

    if matching_buses:
        bus_numbers = ",".join(str(bus_number) for bus_number in matching_buses)
        return redirect(url_for("show_qr_code", bus_numbers=bus_numbers))
    else:
        return "No matching bus found."



@app.route("/logout")
def logout():
    session.clear()  # Clear the session
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)