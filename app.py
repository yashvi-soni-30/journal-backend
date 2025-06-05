# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql.connector
# import os
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# # --- DATABASE CONNECTION ---
# db = mysql.connector.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )

# cursor = db.cursor(dictionary=True)

# # --- SAVE ENTRY ---
# @app.route('/save', methods=['POST'])
# def save_entry():
#     data = request.json
#     user_id = data.get('user_id')
#     text = data.get('text')
#     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     cursor.execute(
#         "INSERT INTO entries (user_id, text, date) VALUES (%s, %s, %s)",
#         (user_id, text, date)
#     )
#     db.commit()
#     return jsonify({"message": "Entry saved successfully"})

# # --- GET ENTRIES ---
# @app.route('/entries/<int:user_id>', methods=['GET'])
# def get_entries(user_id):
#     cursor.execute("SELECT * FROM entries WHERE user_id = %s ORDER BY date DESC", (user_id,))
#     return jsonify(cursor.fetchall())

# # --- EDIT ENTRY ---
# @app.route('/edit/<int:entry_id>', methods=['PUT'])
# def edit_entry(entry_id):
#     data = request.json
#     text = data.get('text')
#     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     cursor.execute("UPDATE entries SET text = %s, date = %s WHERE id = %s", (text, date, entry_id))
#     db.commit()
#     return jsonify({"message": "Entry updated"})

# # --- DELETE ENTRY ---
# @app.route('/delete/<int:entry_id>', methods=['DELETE'])
# def delete_entry(entry_id):
#     cursor.execute("DELETE FROM entries WHERE id = %s", (entry_id,))
#     db.commit()
#     return jsonify({"message": "Entry deleted"})

# # --- RUN APP ---
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION ---
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),         # e.g., 'mysql-<yourusername>.alwaysdata.net'
    user=os.getenv("DB_USER"),         # e.g., '<yourusername>'
    password=os.getenv("DB_PASSWORD"), # your DB password
    database=os.getenv("DB_NAME")      # e.g., '<yourusername>_journaldb'
)
cursor = db.cursor(dictionary=True)

# --- REGISTER ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"error": "User already exists"}), 400

    # Create new user
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    db.commit()
    return jsonify({"message": "User registered successfully"}), 201

# --- LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    if user:
        return jsonify({"user_id": user['id']})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# --- SAVE ENTRY ---
@app.route('/save', methods=['POST'])
def save_entry():
    data = request.json
    user_id = data.get('user_id')
    text = data.get('text')
    date = data.get('date') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO entries (user_id, text, date) VALUES (%s, %s, %s)",
        (user_id, text, date)
    )
    db.commit()
    return jsonify({"message": "Entry saved successfully"})

# --- GET ENTRIES ---
@app.route('/entries/<int:user_id>', methods=['GET'])
def get_entries(user_id):
    cursor.execute("SELECT * FROM entries WHERE user_id = %s ORDER BY date DESC", (user_id,))
    return jsonify(cursor.fetchall())

# --- EDIT ENTRY ---
@app.route('/edit/<int:entry_id>', methods=['PUT'])
def edit_entry(entry_id):
    data = request.json
    text = data.get('text')
    date = data.get('date') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("UPDATE entries SET text = %s, date = %s WHERE id = %s", (text, date, entry_id))
    db.commit()
    return jsonify({"message": "Entry updated"})

# --- DELETE ENTRY ---
@app.route('/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    cursor.execute("DELETE FROM entries WHERE id = %s", (entry_id,))
    db.commit()
    return jsonify({"message": "Entry deleted"})

# --- RUN APP ---
if __name__ == '__main__':
    app.run(debug=True)

