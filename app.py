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

# --- DATABASE CONNECTION FUNCTION ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# --- REGISTER ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "User already exists"}), 400

        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if db.is_connected():
            db.close()

# --- LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"user_id": user['id']})
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if db.is_connected():
            db.close()

# --- SAVE ENTRY ---
@app.route('/save', methods=['POST'])
def save_entry():
    data = request.json
    user_id = data.get('user_id')
    text = data.get('text')
    date = data.get('date') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO entries (user_id, text, date) VALUES (%s, %s, %s)",
            (user_id, text, date)
        )
        db.commit()
        return jsonify({"message": "Entry saved successfully"})

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if db.is_connected():
            db.close()

# --- GET ENTRIES ---
@app.route('/entries/<int:user_id>', methods=['GET'])
def get_entries(user_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM entries WHERE user_id = %s ORDER BY date DESC", (user_id,))
        return jsonify(cursor.fetchall())

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if db.is_connected():
            db.close()

# --- EDIT ENTRY ---
@app.route('/edit/<int:entry_id>', methods=['PUT'])
def edit_entry(entry_id):
    data = request.json
    text = data.get('text')
    date = data.get('date') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("UPDATE entries SET text = %s, date = %s WHERE id = %s", (text, date, entry_id))
        db.commit()
        return jsonify({"message": "Entry updated"})

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if db.is_connected():
            db.close()

# --- DELETE ENTRY ---
@app.route('/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("DELETE FROM entries WHERE id = %s", (entry_id,))
        db.commit()
        return jsonify({"message": "Entry deleted"})

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if db.is_connected():
            db.close()

# --- RUN APP ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
