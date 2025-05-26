from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from flask import request, jsonify
import jwt
import datetime
from flask import current_app
import logging
from Database_Connection import Database
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()  # ✅ load .env into environment



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"],supports_credentials=True)  # ✅ enable credentials
app.secret_key = 'your-secret-key'


def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
@app.route('/')
def home():
    return "✅ Flask app is running on Render!"

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(' ')[1]
        user = verify_token(token)

        if user == "EXPIRED":
            return jsonify({"error": "Token expired"}), 401
        elif not user:
            return jsonify({"error": "Invalid token"}), 401

        request.user = user
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["POST"])
def login():
    logger.info("Login function was triggered")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    connect_obj = Database()
    user_data = connect_obj.get_user_by_name(username)

    if user_data[3] == str(password):
        logger.info(user_data[3] + str(password))
        token=generate_token(username)
        return jsonify({"success": True, "message": "Login successful", "token": token})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.info("Register was called")

    if request.method == 'POST':
        data=request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        connect_obj=Database()
        print(name)
        connect_obj.insert_user(name,email,password)
        # Use email as the unique identifier
    return jsonify({"success": True}), 200


@app.route("/logout", methods=["POST"])
def logout():
    print("Session was cleared")
    return jsonify({"message": "Logged out"})

@app.route('/cart/update', methods=['POST'])
@jwt_required
def update_cart():
    user_email = request.user  # ✅ comes from JWT payload
    data = request.get_json()
    print(data)
    print("Above is the data")
    book_id = int(data['book_id'])
    quantity = int(data['quantity'])

    db = Database()
    user = db.get_user_by_name(user_email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user[0]

    if quantity > 0:
        db.upsert_cart(user_id, book_id, quantity)
    else:
        db.remove_from_cart(user_id, book_id)

    # Optional debug/logging
    db.get_all_employees()
    db.get_all_user_cart()

    return jsonify({'status': 'updated'})



def generate_token(user_email):
    payload = {
        'user': user_email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
