from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import json
from Database_Connection import Database
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()  # ✅ load .env into environment


app = Flask(__name__)
CORS(app, supports_credentials=True)  # ✅ enable credentials
app.secret_key = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.permanent_session_lifetime=timedelta(minutes=30)

# Load users
with open("users.json") as f:
    users = json.load(f)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    connect_obj = Database()
    user_data = connect_obj.get_user_by_name(username)

    if user_data[3] == str(password):
        session.permanent = True
        print(request.cookies.get('session'))
        session['user'] = user_data[1]
        session['cart'] = []
        print("User was", session.get("user"))
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/me", methods=["GET"])
def me():
    if 'user' in session:
        return jsonify({"loggedIn": True, "username": session['user']})
    return jsonify({"loggedIn": False}), 401

@app.route("/logout", methods=["POST"])
def logout():
    print("Session was cleared")
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route('/cart/update', methods=['POST'])
def update_cart():
    print(request.get_json())
    print("User was", session.get("user"))

    if 'user' not in session:
        return {'status': 'unauthorized'}, 401

    data = request.json
    book_id = int(data['book_id'])
    quantity = int(data['quantity'])

    db = Database()
    user = db.get_user_by_name(session.get('user'))

    user_id = user[0]

    if quantity > 0:
        db.upsert_cart(user_id, book_id, quantity)
    else:
        db.remove_from_cart(user_id, book_id)

    db.get_all_employees()

    # Print all cart items
    db.get_all_user_cart()
    return {'status': 'updated'}




if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)