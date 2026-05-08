from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3
import re
import json
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_helper import DBHelper
from utils.ai_engine import analyze_idea

DBHelper.init_db()
app = Flask(__name__)
app.secret_key = 'i2i_secure_key_2026'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    idea = data.get("idea")

    result = analyze_idea(idea)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ideas 
        (user_id, original_idea, improved_idea, domain, uniqueness_score, ai_response)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
        session['user_id'],
        idea,
        result['improvedIdea'],
        result['domain'],
        result['uniquenessScore'],
        json.dumps(result)
    ))

    idea_id = cursor.lastrowid   
    conn.commit()
    conn.close()

    result['idea_id'] = idea_id

    return jsonify(result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
      
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if len(password) < 8:
            return "Error: Password must be at least 8 characters long!", 400
    
        if not re.match(r"^[A-Za-z0-9@$#%&*^!]+$", password):
            return "Error: Password contains invalid characters!", 400

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO users (username, email, password)
                           VALUES (?, ?, ?)
                           """, (username, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close() 
            return render_template('email_already_existed.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password_candidate):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect ('/dashboard')
        else:
            return render_template('unauthorized.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])

@app.route('/favorite', methods=['POST'])
def favorite():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    idea_id = data.get("idea_id")
    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM favorites 
        WHERE user_id = ? AND idea_id = ?
    """, (user_id, idea_id))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            DELETE FROM favorites 
            WHERE user_id = ? AND idea_id = ?
        """, (user_id, idea_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "removed"})
    else:
        cursor.execute("""
            INSERT INTO favorites (user_id, idea_id)
            VALUES (?, ?)
        """, (user_id, idea_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "added"})

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, original_idea, domain, uniqueness_score, created_at
        FROM ideas
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    ideas = cursor.fetchall()

    cursor.execute("""
        SELECT ideas.id, ideas.original_idea, ideas.domain, ideas.uniqueness_score, ideas.created_at
        FROM ideas
        JOIN favorites ON ideas.id = favorites.idea_id
        WHERE favorites.user_id = ?
        ORDER BY ideas.created_at DESC
    """, (user_id,))
    favorites = cursor.fetchall()

    conn.close()

    return render_template("history.html", ideas=ideas, favorites=favorites)

@app.route('/delete_idea', methods=['POST'])
def delete_idea():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    idea_id = data.get("idea_id")
    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM ideas 
        WHERE id = ? AND user_id = ?
    """, (idea_id, user_id))

    idea = cursor.fetchone()

    if not idea:
        conn.close()
        return jsonify({"error": "Not allowed"}), 403

    cursor.execute("""
        DELETE FROM favorites WHERE idea_id = ?
    """, (idea_id,))

    cursor.execute("""
        DELETE FROM ideas WHERE id = ?
    """, (idea_id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})

@app.route('/idea/<int:idea_id>')
def idea_detail(idea_id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ai_response FROM ideas 
        WHERE id = ? AND user_id = ?
    """, (idea_id, session['user_id']))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return "Not found", 404

    data = json.loads(row[0])

    return render_template("idea_detail.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)