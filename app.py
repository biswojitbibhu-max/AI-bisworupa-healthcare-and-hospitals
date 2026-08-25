from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash
)

import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)

app.secret_key = "bisworupa-healthcare-secret-key"

DATABASE = "database.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =====================================================
# INITIALIZE DATABASE
# =====================================================

def init_db():

    db = get_db()

    # -------------------------------------------------
    # USERS TABLE
    # -------------------------------------------------

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # -------------------------------------------------
    # DOCTORS TABLE
    # -------------------------------------------------

    db.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            qualification TEXT NOT NULL
        )
    """)

    # -------------------------------------------------
    # APPOINTMENTS TABLE
    # -------------------------------------------------

    db.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            message TEXT,

            FOREIGN KEY(user_id)
                REFERENCES users(id),

            FOREIGN KEY(doctor_id)
                REFERENCES doctors(id)
        )
    """)

    # -------------------------------------------------
    # SAMPLE DOCTORS
    # -------------------------------------------------

    count = db.execute(
        "SELECT COUNT(*) AS total FROM doctors"
    ).fetchone()["total"]

    if count == 0:

        doctors = [

            (
                "Dr. Biswojit Sahoo",
                "Cardiology",
                "MBBS, MD Cardiology"
            ),

            (
                "Dr. Saumika Sahoo",
                "General Medicine",
                "MBBS, MD Medicine"
            ),

            (
                "Dr. Subhajit Sahoo",
                "Orthopedics",
                "MBBS, MS Orthopedics"
            ),

            (
                "Dr. Saubhagya Sahoo",
                "Pediatrics",
                "MBBS, MD Pediatrics"
            ),

            (
                "Dr. Pratap Kumar Swain",
                "Dermatology",
                "MBBS, MD Dermatology"
            )
        ]

        db.executemany("""
            INSERT INTO doctors
            (name, department, qualification)
            VALUES (?, ?, ?)
        """, doctors)

    db.commit()
    db.close()


# =====================================================
# AI CHATBOT
# =====================================================

def chatbot_response(message):

    message = message.lower().strip()

    if not message:
        return "Please enter your question."

    if any(word in message for word in ["hello", "hi", "hey"]):

        return (
            "Hello! 👋 Welcome to Bisworupa Healthcare. "
            "I am your healthcare assistant. "
            "How can I help you?"
        )

    if "appointment" in message or "book" in message:

        return (
            "You can book an appointment from the "
            "Appointments page. Please select a doctor, "
            "date and time."
        )

    if "doctor" in message:

        return (
            "We have doctors in Cardiology, General Medicine, "
            "Orthopedics, Pediatrics and Dermatology."
        )

    if "cardiology" in message or "heart" in message:

        return (
            "Our Cardiology department provides care related "
            "to heart and cardiovascular conditions. "
            "Please consult a qualified cardiologist for "
            "medical advice."
        )

    if "pediatric" in message or "child" in message:

        return (
            "Our Pediatrics department provides healthcare "
            "for children. Please consult a pediatrician "
            "for specific medical concerns."
        )

    if "skin" in message or "dermatology" in message:

        return (
            "Our Dermatology department deals with skin, "
            "hair and nail concerns. A dermatologist can "
            "provide an appropriate evaluation."
        )

    if "bone" in message or "orthopedic" in message:

        return (
            "Our Orthopedics department provides care for "
            "bones, joints and musculoskeletal conditions."
        )

    if "emergency" in message:

        return (
            "If you are experiencing a medical emergency, "
            "seek immediate emergency medical care or "
            "contact your local emergency service. "
            "Do not rely on this chatbot for emergency care."
        )

    if "contact" in message:

        return (
            "You can find Bisworupa Healthcare contact "
            "information on the Contact Us page."
        )

    if "location" in message or "address" in message:

        return (
            "You can find the Bisworupa Healthcare location "
            "on our Location page."
        )

    if "thank" in message:

        return "You're welcome! Stay healthy. 😊"

    if "bye" in message:

        return "Goodbye! Take care and stay healthy."

    return (
        "I can help with general information about "
        "Bisworupa Healthcare, doctors, departments "
        "and appointments. For diagnosis or treatment, "
        "please consult a qualified healthcare professional."
    )


# =====================================================
# HOME
# =====================================================

@app.route("/")
def index():

    return render_template("index.html")


# =====================================================
# CHATBOT
# =====================================================

@app.route("/chatbot")
def chatbot():

    return render_template("chatbot.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    response = chatbot_response(message)

    return jsonify({
        "response": response
    })


# =====================================================
# DOCTORS
# =====================================================

@app.route("/doctors")
def doctors():

    db = get_db()

    doctors = db.execute(
        "SELECT * FROM doctors"
    ).fetchall()

    db.close()

    return render_template(
        "doctors.html",
        doctors=doctors
    )


# =====================================================
# EDIT DOCTOR
# =====================================================

@app.route(
    "/edit-doctor/<int:doctor_id>",
    methods=["GET", "POST"]
)
def edit_doctor(doctor_id):

    db = get_db()

    doctor = db.execute(
        "SELECT * FROM doctors WHERE id = ?",
        (doctor_id,)
    ).fetchone()

    if doctor is None:

        db.close()

        flash("Doctor not found.")

        return redirect(
            url_for("doctors")
        )

    if request.method == "POST":

        name = request.form.get(
            "name", ""
        ).strip()

        department = request.form.get(
            "department", ""
        ).strip()

        qualification = request.form.get(
            "qualification", ""
        ).strip()

        if not name or not department or not qualification:

            db.close()

            flash(
                "Please fill all doctor details."
            )

            return redirect(
                url_for(
                    "edit_doctor",
                    doctor_id=doctor_id
                )
            )

        db.execute("""
            UPDATE doctors

            SET
                name = ?,
                department = ?,
                qualification = ?

            WHERE id = ?
        """, (
            name,
            department,
            qualification,
            doctor_id
        ))

        db.commit()
        db.close()

        flash(
            "Doctor information updated successfully."
        )

        return redirect(
            url_for("doctors")
        )

    db.close()

    return render_template(
        "edit_doctor.html",
        doctor=doctor
    )


# =====================================================
# REGISTER
# =====================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        if not name or not email or not password:

            flash("Please fill all fields.")

            return redirect(
                url_for("register")
            )

        hashed_password = generate_password_hash(
            password
        )

        db = get_db()

        try:

            db.execute("""
                INSERT INTO users
                (name, email, password)

                VALUES (?, ?, ?)
            """, (
                name,
                email,
                hashed_password
            ))

            db.commit()

            flash(
                "Registration successful. Please login."
            )

            return redirect(
                url_for("login")
            )

        except sqlite3.IntegrityError:

            flash(
                "Email already registered."
            )

            return redirect(
                url_for("register")
            )

        finally:

            db.close()

    return render_template(
        "register.html"
    )


# =====================================================
# LOGIN
# =====================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        db = get_db()

        user = db.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        db.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password."
        )

    return render_template(
        "login.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash("Please login first.")

        return redirect(
            url_for("login")
        )

    db = get_db()

    appointments = db.execute("""
        SELECT
            appointments.*,
            doctors.name AS doctor_name,
            doctors.department

        FROM appointments

        JOIN doctors
        ON appointments.doctor_id = doctors.id

        WHERE appointments.user_id = ?

        ORDER BY
            appointment_date,
            appointment_time
    """, (
        session["user_id"],
    )).fetchall()

    db.close()

    return render_template(
        "dashboard.html",
        appointments=appointments
    )


# =====================================================
# APPOINTMENTS
# =====================================================

@app.route(
    "/appointments",
    methods=["GET", "POST"]
)
def appointments():

    if "user_id" not in session:

        flash(
            "Please login to book an appointment."
        )

        return redirect(
            url_for("login")
        )

    db = get_db()

    doctors = db.execute(
        "SELECT * FROM doctors"
    ).fetchall()

    if request.method == "POST":

        doctor_id = request.form.get(
            "doctor_id"
        )

        appointment_date = request.form.get(
            "appointment_date"
        )

        appointment_time = request.form.get(
            "appointment_time"
        )

        message = request.form.get(
            "message", ""
        )

        if not doctor_id or not appointment_date or not appointment_time:

            db.close()

            flash(
                "Please select doctor, date and time."
            )

            return redirect(
                url_for("appointments")
            )

        db.execute("""
            INSERT INTO appointments
            (
                user_id,
                doctor_id,
                appointment_date,
                appointment_time,
                message
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            doctor_id,
            appointment_date,
            appointment_time,
            message
        ))

        db.commit()

        db.close()

        flash(
            "Appointment booked successfully."
        )

        return redirect(
            url_for("dashboard")
        )

    db.close()

    return render_template(
        "appointments.html",
        doctors=doctors
    )


# =====================================================
# CONTACT
# =====================================================

@app.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# =====================================================
# LOCATION
# =====================================================

@app.route("/location")
def location():

    return render_template(
        "location.html"
    )


# =====================================================
# ABOUT
# =====================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =====================================================
# BLOGS
# =====================================================

@app.route("/blogs")
def blogs():

    return render_template(
        "blogs.html"
    )


# =====================================================
# CAREERS
# =====================================================

@app.route("/careers")
def careers():

    return render_template(
        "careers.html"
    )


# =====================================================
# AWARDS
# =====================================================

@app.route("/awards")
def awards():

    return render_template(
        "awards.html"
    )


# =====================================================
# MEDIA
# =====================================================

@app.route("/media")
def media():

    return render_template(
        "media.html"
    )


# =====================================================
# FEEDBACK
# =====================================================

@app.route("/feedback")
def feedback():

    return render_template(
        "feedback.html"
    )


# =====================================================
# BRAND COLLABORATION
# =====================================================

@app.route("/brand-collaboration")
def brand_collaboration():

    return render_template(
        "brand_collaboration.html"
    )


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )