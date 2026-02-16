from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bharath@18",
    database="hospital_management"
)

# Home route
@app.route("/")
def home():
    return render_template("index.html")  # Make sure index.html is in a "templates" folder

# API to add a new patient
@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.json
    try:
        cursor = db.cursor()
        query = """
            INSERT INTO patients (name, age, gender, phone, doctor)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data["name"], data["age"], data["gender"], data["phone"], data["doctor"]))
        db.commit()
        return jsonify({"message": "Patient added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to get all patients
@app.route("/patients", methods=["GET"])
def get_patients():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

