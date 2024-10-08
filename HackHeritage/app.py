# load packages==============================================================
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import sqlite3
from decouple import config
app = Flask(__name__)
app.secret_key = config("app.secret_key")
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()
# Load the scaler, label encoder, model, and class names=====================
scaler = pickle.load(open("Models/scaler.pkl", 'rb'))
model = pickle.load(open("Models/model.pkl", 'rb'))
class_names = ['Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown',
               'Software Engineer', 'Teacher', 'Business Owner', 'Scientist',
               'Banker', 'Writer', 'Accountant', 'Designer',
               'Construction Engineer', 'Game Developer', 'Stock Investor',
               'Real Estate Developer']

# Recommendations ===========================================================
def Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                    weekly_self_study_hours, math_score, history_score, physics_score,
                    chemistry_score, biology_score, english_score, geography_score,
                    total_score, average_score):
    # Encode categorical variables
    gender_encoded = 1 if gender.lower() == 'female' else 0
    part_time_job_encoded = 1 if part_time_job else 0
    extracurricular_activities_encoded = 1 if extracurricular_activities else 0

    # Create feature array
    feature_array = np.array([[gender_encoded, part_time_job_encoded, absence_days, extracurricular_activities_encoded,
                               weekly_self_study_hours, math_score, history_score, physics_score,
                               chemistry_score, biology_score, english_score, geography_score, total_score,
                               average_score]])

    # Scale features
    scaled_features = scaler.transform(feature_array)

    # Predict using the model
    probabilities = model.predict_proba(scaled_features)

    # Get top three predicted classes along with their probabilities
    top_classes_idx = np.argsort(-probabilities[0])[:3]
    top_classes_names_probs = [(class_names[idx], probabilities[0][idx]) for idx in top_classes_idx]

    return top_classes_names_probs
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash("Invalid login credentials. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # Generate the password hash using the default method
            hashed_password = generate_password_hash(password)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()

            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        else:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))
@app.route('/career_graph')
def career_graph():
    return render_template('career_graph.html')
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/science')
def science():
    return render_template('science.html')

@app.route('/commerce')
def commerce():
    return render_template('commerce.html')

@app.route('/cse')
def cse():
    return render_template('cse.html')
@app.route('/me')
def me():
    return render_template('me.html')
@app.route('/ce')
def ce():
    return render_template('ce.html')
@app.route('/ee')
def ee():
    return render_template('ee.html')
@app.route('/ece')
def ece():
    return render_template('ece.html')
@app.route('/generalmedicine')
def generalmedicine():
    return render_template('generalmedicine.html')
@app.route('/surgery')
def surgery():
    return render_template('surgery.html')
@app.route('/pediatrics')
def pediatrics():
    return render_template('pediatrics.html')
@app.route('/gynecology')
def gynecology():
    return render_template('gynecology.html')

@app.route('/arts')
def arts():
    return render_template('arts.html')
@app.route('/orthopedics')
def orthopedics():
    return render_template('orthopedics.html')
@app.route('/Physics')
def physics():
    return render_template('Physics.html')
@app.route('/chemistry')
def chemistry():
    return render_template('chemistry.html')
@app.route('/math')
def math():
    return render_template('math.html')
@app.route('/evs_sc')
def evs_sc():
    return render_template('evs_sc.html')
@app.route('/biology')
def biology():
    return render_template('biology.html')
@app.route('/cost_acc')
def cost_acc():
    return render_template('cost_acc.html')
@app.route('/fin_acc')
def fin_acc():
    return render_template('fin_acc.html')
@app.route('/manage_acc')
def manage_acc():
    return render_template('manage_acc.html')
@app.route('/audit')
def audit():
    return render_template('audit.html')
@app.route('/tax')
def tax():
    return render_template('tax.html')
@app.route('/hr')
def hr():
    return render_template('hr.html')
@app.route('/operations_manage')
def operations_manage():
    return render_template('operations_manage.html')
@app.route('/fin_manage')
def fin_manage():
    return render_template('fin_manage.html')
@app.route('/market_manage')
def market_manage():
    return render_template('market_manage.html')
@app.route('/strat_manage')
def strat_manage():
    return render_template('strat_manage.html')
@app.route('/pred', methods=['POST','GET'])
def pred():
    if request.method == 'POST':
        gender = request.form['gender']
        part_time_job = request.form['part_time_job'] == 'true'
        absence_days = int(request.form['absence_days'])
        extracurricular_activities = request.form['extracurricular_activities'] == 'true'
        weekly_self_study_hours = int(request.form['weekly_self_study_hours'])
        math_score = int(request.form['math_score'])
        history_score = int(request.form['history_score'])
        physics_score = int(request.form['physics_score'])
        chemistry_score = int(request.form['chemistry_score'])
        biology_score = int(request.form['biology_score'])
        english_score = int(request.form['english_score'])
        geography_score = int(request.form['geography_score'])
        total_score = float(request.form['total_score'])
        average_score = float(request.form['average_score'])

        recommendations = Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                                          weekly_self_study_hours, math_score, history_score, physics_score,
                                          chemistry_score, biology_score, english_score, geography_score,
                                          total_score, average_score)

        return render_template('results.html', recommendations=recommendations)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
