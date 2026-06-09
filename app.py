from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        dob TEXT NOT NULL,
        email TEXT NOT NULL,
        glucose REAL NOT NULL,
        haemoglobin REAL NOT NULL,
        cholesterol REAL NOT NULL,
        remarks TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# AI Prediction Logic
def predict_health(glucose, haemoglobin, cholesterol):

    glucose = float(glucose)
    haemoglobin = float(haemoglobin)
    cholesterol = float(cholesterol)

    if glucose > 140 and cholesterol > 240:
        return "High risk of diabetes and cardiovascular disease"

    elif haemoglobin < 12:
        return "Possible anemia detected"

    elif cholesterol > 240:
        return "High cholesterol level detected"

    else:
        return "Health indicators appear normal"


# Home Page - Display Patients
@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template('index.html', patients=patients)


# Add Patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients
        (fullname, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fullname,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_patient.html')


# Edit Patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        if dob > "2026-06-09":
          return "Date of Birth cannot be a future date"
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        cursor.execute("""
        UPDATE patients
        SET fullname=?,
            dob=?,
            email=?,
            glucose=?,
            haemoglobin=?,
            cholesterol=?,
            remarks=?
        WHERE id=?
        """,
        (
            fullname,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (id,)
    )

    patient = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_patient.html',
        patient=patient
    )


# Delete Patient
@app.route('/delete/<int:id>')
def delete_patient(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)