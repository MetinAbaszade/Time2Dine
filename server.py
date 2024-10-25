from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
import mysql.connector, datetime
from sshtunnel import SSHTunnelForwarder
import jwt, datetime
from functools import wraps


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
 # JWT secret key
SECRET_KEY = 'QABIL TURKOQLU' 

# # Set up SSH tunnel with a different local bind port
# tunnel = SSHTunnelForwarder(
#     ('5.75.182.107', 22),  
#     ssh_username='bgazanfar',  
#     ssh_password='MdEbbp',
#     remote_bind_address=('127.0.0.1', 3306),
#     local_bind_address=('127.0.0.1', 10022),  
#     set_keepalive=60
# )

# # Start the SSH tunnel
# tunnel.start()

db_config = {
    'host': '127.0.0.1',
    'user': 'bgazanfar',
    'password': 'MdEbbp',
    'database': 'bgazanfar_db',
    #'port': tunnel.local_bind_port, 
    'connection_timeout': 10  
}

@app.route('/')
def root():
    return send_from_directory('static', 'index.htm')

@app.route('/index.htm')
def serve_index():
    return send_from_directory('static', 'index.htm')

@app.route('/login.htm')
def serve_login():
    return send_from_directory('static', 'login.htm')

@app.route('/register.htm')
def serve_register():
    return send_from_directory('static', 'register.htm')

@app.route('/restaurant.htm')
def serve_restaurant():
    return send_from_directory('static', 'restaurant.htm')

@app.route('/fav.htm')
def serve_fav():
    return send_from_directory('static', 'fav.htm')

@app.route('/imprint.htm')
def serve_imprint():
    return send_from_directory('static', 'imprint.htm')


def extract_user_id_from_token():
    token = request.headers.get('Authorization')
    # Extract the token after "Bearer"
    token = token.split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    # Extract the userId from the payload
    user_id = data['userId']  
    return user_id

def generate_jwt_token(user_id):
    payload = {
        'userId': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(" ")[1] 
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated

def get_db_connection():
    print(f"Tunnel is active: {tunnel.is_active}")
    print(f"Local bind port: {tunnel.local_bind_port}")
    test= mysql.connector.connect(**db_config)
    return test

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    password = data['password']
    date_of_birth = data['dateOfBirth']
    phone_number = data['phoneNumber']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        user_query = """
            INSERT INTO users (FirstName, LastName, Email, Password, DateOfBirth, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(user_query, (first_name, last_name, email, password, date_of_birth, phone_number))

        # Get the User ID generated by the database
        user_id_query = "SELECT Id FROM Users WHERE Email = %s"
        cursor.execute(user_id_query, (email,))
        user_id = cursor.fetchone()[0]

        customer_query = """
            INSERT INTO Customer (UserId)
            VALUES (%s)
        """
        cursor.execute(customer_query, (user_id,))

        conn.commit()
        return jsonify({'message': 'User and Customer added successfully'}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Join the Users and Customer tables to retrieve Customer.Id
        login_query = """
            SELECT c.Id as customer_Id
            FROM users u
            JOIN customer c ON u.Id = c.UserId
            WHERE u.Email = %s AND u.Password = %s
        """
        cursor.execute(login_query, (email, password))
        customer = cursor.fetchone()

        if customer:
            customer_id = customer[0]  # Assuming the first element is customer_Id
            token = generate_jwt_token(customer_id)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'customerId': customer_id  # Send customer_Id instead of user_id
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/toggle_favorite', methods=['POST'])
@token_required
def toggle_favorite():
    user_id = extract_user_id_from_token()
    data = request.json
    food_spot_id = data['foodSpotId']
    print(f"favourites e sorqu gelidiiididididi: {user_id} \n {food_spot_id}")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        check_favorite_query = """
            SELECT * FROM favorites WHERE FoodSpotId = %s AND CustomerId = %s
        """
        cursor.execute(check_favorite_query, (food_spot_id, user_id))
        favorite = cursor.fetchone()

        if favorite:
            remove_favorite_query = """
                DELETE FROM favorites WHERE FoodSpotId = %s AND CustomerId = %s
            """
            cursor.execute(remove_favorite_query, (food_spot_id, user_id))
            conn.commit()
            return jsonify({'message': 'Removed from favorites successfully'}), 200
        else:
            add_favorite_query = """
                INSERT INTO favorites (FoodSpotId, CustomerId)
                VALUES (%s, %s)
            """
            cursor.execute(add_favorite_query, (food_spot_id, user_id))
            conn.commit()
            return jsonify({'message': 'Added to favorites successfully'}), 201

    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_favorites', methods=['GET'])
@token_required
def get_favorites():
    user_id = extract_user_id_from_token()
    search_query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        favorites_query = """
            SELECT fs.Id AS FoodSpotId, 
                   fs.Name, 
                   fs.Rating, 
                   fs.ImageUrl, 
                   CASE 
                       WHEN r.Id IS NOT NULL THEN 'Restaurant'
                       WHEN c.Id IS NOT NULL THEN 'Cafe'
                       ELSE 'Unknown'
                   END AS FoodSpotType,
                   COALESCE(r.Id, c.Id) AS TypeSpecificId,
                   TRUE AS isFavorite  -- Always true since this is the favorites list
            FROM favorites f
            JOIN foodspot fs ON f.FoodSpotId = fs.Id
            LEFT JOIN restaurant r ON fs.Id = r.FoodSpotId
            LEFT JOIN cafe c ON fs.Id = c.FoodSpotId
            WHERE f.CustomerId = %s
        """

        # If a search query is provided, add a LIKE clause to filter by name
        if search_query:
            favorites_query += " AND fs.Name LIKE %s"
            cursor.execute(favorites_query, (user_id, f'%{search_query}%'))
        else:
            cursor.execute(favorites_query, (user_id,))

        favorites = cursor.fetchall()

        # Convert any datetime or timedelta values to strings for JSON serialization
        for favorite in favorites:
            for key, value in favorite.items():
                if isinstance(value, (datetime.datetime, datetime.date, datetime.timedelta)):
                    favorite[key] = str(value)

        return jsonify(favorites), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_foodspots', methods=['GET'])
@token_required
def get_foodspots():
    search_query = request.args.get('q', '') 
    user_id = extract_user_id_from_token()   
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        foodspots_query = """
            SELECT fs.Id AS FoodSpotId, fs.Name, fs.Rating, fs.ImageUrl, 
                   CASE 
                       WHEN r.Id IS NOT NULL THEN 'Restaurant'
                       WHEN c.Id IS NOT NULL THEN 'Cafe'
                       ELSE 'Unknown'
                   END AS FoodSpotType,
                   r.Id AS RestaurantId,
                   c.Id AS CafeId,
                   CASE 
                       WHEN f.CustomerId IS NOT NULL THEN TRUE
                       ELSE FALSE
                   END AS IsFavorite
            FROM foodspot fs
            LEFT JOIN restaurant r ON fs.Id = r.FoodSpotId
            LEFT JOIN cafe c ON fs.Id = c.FoodSpotId
            LEFT JOIN favorites f ON fs.Id = f.FoodSpotId AND f.CustomerId = %s
            WHERE fs.Name LIKE %s
        """
        cursor.execute(foodspots_query, (user_id, '%' + search_query + '%'))  
        foodspots = cursor.fetchall()

        for spot in foodspots:
            for key, value in spot.items():
                if isinstance(value, (datetime.timedelta, datetime.datetime, datetime.date)):
                    spot[key] = str(value)  

        return jsonify(foodspots), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_foodspot/<foodspot_id>', methods=['GET'])
@token_required
def get_foodspot(foodspot_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        foodspot_query = """
            SELECT fs.Id AS FoodSpotId, fs.*, 
                   CASE 
                       WHEN r.Id IS NOT NULL THEN 'Restaurant'
                       WHEN c.Id IS NOT NULL THEN 'Cafe'
                       ELSE 'Unknown'
                   END AS FoodSpotType,
                   r.Id AS RestaurantId,
                   c.Id AS CafeId
            FROM foodspot fs
            LEFT JOIN restaurant r ON fs.Id = r.FoodSpotId
            LEFT JOIN cafe c ON fs.Id = c.FoodSpotId
            WHERE fs.Id = %s
        """
        cursor.execute(foodspot_query, (foodspot_id,))
        foodspot = cursor.fetchone()

        if foodspot:
            for key, value in foodspot.items():
                if isinstance(value, (datetime.datetime, datetime.date, datetime.timedelta)):
                    foodspot[key] = str(value)
            return jsonify(foodspot), 200
        else:
            return jsonify({'error': 'FoodSpot not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8024, debug=True)