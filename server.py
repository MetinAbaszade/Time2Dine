import re
import requests
import jwt, datetime
from functools import wraps
from flask_cors import CORS 
import mysql.connector, datetime
from sshtunnel import SSHTunnelForwarder
from flask import Flask, request, jsonify, send_from_directory, send_file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
 # JWT secret key
SECRET_KEY = 'QABIL TURKOQLU' 
ERROR_LOG_FILE_PATH = '/var/log/apache2/error.log'
ACCESS_LOG_FILE_PATH = '/var/log/apache2/access.log'

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

def parse_error_log(file_path):
    log_entries = []
    error_log_pattern = re.compile(
        r'\[(?P<date>.+?)\] \[(?P<module>.+?):(?P<level>.+?)\](?: \[pid (?P<pid>\d+)\])? (?P<message>.+)'
    )
    with open(file_path, 'r') as file:
        for line in file:
            match = error_log_pattern.match(line)
            if match:
                entry = match.groupdict()
                # Remove keys with None values (like pid for notice logs)
                entry = {k: v for k, v in entry.items() if v is not None}
                log_entries.append(entry)
    return log_entries

def parse_access_log(file_path):
    log_entries = []
    access_log_pattern = re.compile(
        r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>[A-Z]+) (?P<path>[^\s]+) (?P<protocol>HTTP/[\d\.]+)" '
        r'(?P<status>\d{3}) (?P<bytes>\d+) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )
    with open(file_path, 'r') as file:
        for line in file:
            match = access_log_pattern.match(line)
            if match:
                log_entries.append(match.groupdict())
    return log_entries

@app.route('/')
def root():
    return send_from_directory('static', 'index.htm')

@app.route('/admin')
def serve_admin():
    return send_from_directory('static', 'admin.htm')

@app.route('/admin.htm')
def server_admin_page():
    return send_from_directory('static', 'admin.htm')

@app.route('/restaurant_add.htm')
def serve_restaurant_add_page():
    return send_from_directory('static', 'restaurant_add.htm')

@app.route('/user_add.htm')
def serve_user_add_page():
    return send_from_directory('static', 'user_add.htm')

@app.route('/user_edit.htm')
def serve_user_edit_page():
    return send_from_directory('static', 'user_edit.htm')

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

@app.route('/restaurant_edit.htm')
def serve_restaurant_edit():
    return send_from_directory('static', 'restaurant_edit.htm')

@app.route('/fav.htm')
def serve_fav():
    return send_from_directory('static', 'fav.htm')

@app.route('/imprint.htm')
def serve_imprint():
    return send_from_directory('static', 'imprint.htm')

@app.route('/location.htm')
def serve_location():
    return send_from_directory('static', 'location.htm')

@app.route('/search.htm')
def serve_search():
    return send_from_directory('static', 'search.htm')

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

def is_admin(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the user has an admin role
        admin_query = "SELECT Id FROM admin WHERE UserId = %s"
        cursor.execute(admin_query, (user_id,))
        is_admin = cursor.fetchone() is not None
        return is_admin
    finally:
        cursor.close()
        conn.close()

def get_db_connection():
#     print(f"Tunnel is active: {tunnel.is_active}")
#     print(f"Local bind port: {tunnel.local_bind_port}")
    return mysql.connector.connect(**db_config)

@app.route('/get_all_users', methods=['GET'])
@token_required
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT u.Id AS UserId, u.FirstName, u.LastName, u.Email, u.DateOfBirth, u.PhoneNumber,
                   CASE 
                       WHEN a.Id IS NOT NULL THEN 'Admin'
                       WHEN c.Id IS NOT NULL THEN 'Customer'
                       ELSE 'Unknown'
                   END AS Role
            FROM users u
            LEFT JOIN admin a ON u.Id = a.UserId
            LEFT JOIN customer c ON u.Id = c.UserId
        """
        cursor.execute(query)
        users = cursor.fetchall()

        return jsonify(users), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_user_details/<search_user_id>', methods=['GET'])
@token_required
def get_user_details(search_user_id):
    user_id = extract_user_id_from_token()
    
    # Check if the user is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can add users.'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT u.Id AS UserId, u.FirstName, u.LastName, u.Email, u.DateOfBirth, u.PhoneNumber,
                   CASE 
                       WHEN a.Id IS NOT NULL THEN 1
                       ELSE 0
                   END AS isAdmin
            FROM users u
            LEFT JOIN admin a ON u.Id = a.UserId
            WHERE u.Id = %s
        """
        cursor.execute(query, (search_user_id,))
        user_details = cursor.fetchone()

        if not user_details:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user_details), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/add_user', methods=['POST'])
@token_required
def add_user():
    user_id = extract_user_id_from_token()
    
    # Check if the user is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can add users.'}), 403

    data = request.json
    first_name = data['FirstName']
    last_name = data['LastName']
    email = data['Email']
    password = data['Password']
    date_of_birth = data['DateOfBirth']
    phone_number = data['PhoneNumber']
    # Default to non-admin if not provided
    is_admin_flag = data.get('isAdmin', 0)  

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into Users table
        user_query = """
            INSERT INTO users (FirstName, LastName, Email, Password, DateOfBirth, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(user_query, (first_name, last_name, email, password, date_of_birth, phone_number))

        # Get the newly created User ID
        new_user_id = cursor.lastrowid

        if is_admin_flag:
            admin_query = "INSERT INTO admin (UserId) VALUES (%s)"
            cursor.execute(admin_query, (new_user_id,))

        conn.commit()
        return jsonify({'message': 'User added successfully with role'}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/register_user', methods=['POST'])
def register_user():   
    data = request.json
    first_name = data['FirstName']
    last_name = data['LastName']
    email = data['Email']
    password = data['Password']
    date_of_birth = data['DateOfBirth']
    phone_number = data['PhoneNumber']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into Users table
        user_query = """
            INSERT INTO users (FirstName, LastName, Email, Password, DateOfBirth, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(user_query, (first_name, last_name, email, password, date_of_birth, phone_number))

        # Get the newly created User ID
        new_user_id = cursor.lastrowid

        customer_query = "INSERT INTO customer (UserId) VALUES (%s)"
        cursor.execute(customer_query, (new_user_id,))

        conn.commit()
        return jsonify({'message': 'User registered successfully with role'}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/update_user/<user_id_to_update>', methods=['PUT'])
@token_required
def update_user(user_id_to_update):
    user_id = extract_user_id_from_token()
    
    # Check if the user is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can update users.'}), 403

    data = request.json
    first_name = data.get('FirstName')
    last_name = data.get('LastName')
    email = data.get('Email')
    date_of_birth = data.get('DateOfBirth')
    phone_number = data.get('PhoneNumber')
    is_admin_flag = data.get('isAdmin')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update the Users table
        update_query = "UPDATE users SET "
        fields = []
        values = []

        if first_name:
            fields.append("FirstName = %s")
            values.append(first_name)
        if last_name:
            fields.append("LastName = %s")
            values.append(last_name)
        if email:
            fields.append("Email = %s")
            values.append(email)
        if date_of_birth:
            fields.append("DateOfBirth = %s")
            values.append(date_of_birth)
        if phone_number:
            fields.append("PhoneNumber = %s")
            values.append(phone_number)

        update_query += ", ".join(fields) + " WHERE Id = %s"
        values.append(user_id_to_update)

        cursor.execute(update_query, tuple(values))

        # Handle isAdmin updates
        if is_admin_flag is not None:
            admin_check_query = "SELECT * FROM admin WHERE UserId = %s"
            cursor.execute(admin_check_query, (user_id_to_update,))
            is_admin_exists = cursor.fetchone()

            if is_admin_flag and not is_admin_exists:
                admin_insert_query = "INSERT INTO admin (UserId) VALUES (%s)"
                cursor.execute(admin_insert_query, (user_id_to_update,))
            elif not is_admin_flag and is_admin_exists:
                admin_delete_query = "DELETE FROM admin WHERE UserId = %s"
                cursor.execute(admin_delete_query, (user_id_to_update,))

        conn.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_user/<user_id_to_delete>', methods=['DELETE'])
@token_required
def delete_user(user_id_to_delete):
    user_id = extract_user_id_from_token()
    
    # Check if the requester is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can delete users.'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First, check if the user exists and determine their role
        user_check_query = """
            SELECT u.Id AS UserId,
                   CASE
                       WHEN a.Id IS NOT NULL THEN 'Admin'
                       WHEN c.Id IS NOT NULL THEN 'Customer'
                       ELSE 'Unknown'
                   END AS Role
            FROM users u
            LEFT JOIN admin a ON u.Id = a.UserId
            LEFT JOIN customer c ON u.Id = c.UserId
            WHERE u.Id = %s
        """
        cursor.execute(user_check_query, (user_id_to_delete,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Determine if the user is an admin or customer and delete from the appropriate table
        role = user[1]
        if role == 'Admin':
            delete_admin_query = "DELETE FROM admin WHERE UserId = %s"
            cursor.execute(delete_admin_query, (user_id_to_delete,))
        elif role == 'Customer':
            delete_customer_query = "DELETE FROM customer WHERE UserId = %s"
            cursor.execute(delete_customer_query, (user_id_to_delete,))
        else:
            return jsonify({'error': 'User role not recognized; unable to delete.'}), 400

        # Finally, delete the user from the Users table
        delete_user_query = "DELETE FROM users WHERE Id = %s"
        cursor.execute(delete_user_query, (user_id_to_delete,))

        conn.commit()

        return jsonify({'message': f'{role} deleted successfully'}), 200
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
        login_query = """
        SELECT u.Id AS userId,
        CASE 
            WHEN a.Id IS NOT NULL THEN 1
            ELSE 0
        END AS isAdmin
        FROM users u
        LEFT JOIN admin a ON u.Id = a.UserId
        WHERE u.Email = %s AND u.Password = %s
        """
        cursor.execute(login_query, (email, password))
        result = cursor.fetchone()

        if result:
            user_id = result[0] 
            # 1 if admin, 0 if customer
            is_admin = result[1]   

            # Generate JWT token with user_id
            token = generate_jwt_token(user_id)

            return jsonify({
                'message': 'Login successful',
                'token': token,
                'id': user_id,        
                'isAdmin': is_admin
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

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the user has already marked the food spot as favorite in a single query
        check_favorite_query = """
            SELECT f.* 
            FROM favorites f
            JOIN customer c ON f.CustomerId = c.Id
            WHERE f.FoodSpotId = %s AND c.UserId = %s
        """
        cursor.execute(check_favorite_query, (food_spot_id, user_id))
        favorite = cursor.fetchone()

        if favorite:
            # Remove the favorite if it already exists
            remove_favorite_query = """
                DELETE f
                FROM favorites f
                JOIN customer c ON f.CustomerId = c.Id
                WHERE f.FoodSpotId = %s AND c.UserId = %s
            """
            cursor.execute(remove_favorite_query, (food_spot_id, user_id))
            conn.commit()
            return jsonify({'message': 'Removed from favorites successfully'}), 200
        else:
            # Add the favorite if it doesn't exist
            add_favorite_query = """
                INSERT INTO favorites (FoodSpotId, CustomerId)
                SELECT %s, c.Id
                FROM customer c
                WHERE c.UserId = %s
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
        # Fetch all favorites in a single query by joining with the Customer table
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
                   TRUE AS isFavorite
            FROM favorites f
            JOIN foodspot fs ON f.FoodSpotId = fs.Id
            JOIN customer cu ON f.CustomerId = cu.Id
            LEFT JOIN restaurant r ON fs.Id = r.FoodSpotId
            LEFT JOIN cafe c ON fs.Id = c.FoodSpotId
            WHERE cu.UserId = %s
        """
        if search_query:
            favorites_query += " AND fs.Name LIKE %s"
            cursor.execute(favorites_query, (user_id, f'%{search_query}%'))
        else:
            cursor.execute(favorites_query, (user_id,))

        favorites = cursor.fetchall()

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

@app.route('/autocomplete_favorites', methods=['GET'])
@token_required
def autocomplete_favorites():
    user_id = extract_user_id_from_token()
    search_query = request.args.get('q', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Query to fetch matching favorites based on the search query
        favorites_query = """
            SELECT fs.Name
            FROM favorites f
            JOIN foodspot fs ON f.FoodSpotId = fs.Id
            WHERE f.CustomerId = %s AND fs.Name LIKE %s
        """
        cursor.execute(favorites_query, (user_id, '%' + search_query + '%'))
        favorites = cursor.fetchall()

        # Extract just the names for the autocomplete suggestions
        suggestions = [favorite['Name'] for favorite in favorites]

        return jsonify(suggestions), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/autocomplete_foodspots', methods=['GET'])
@token_required
def autocomplete_foodspots():
    search_query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        foodspots_query = """
            SELECT fs.Name
            FROM foodspot fs
            WHERE fs.Name LIKE %s
        """
        cursor.execute(foodspots_query, ('%' + search_query + '%',))
        foodspots = cursor.fetchall()

        suggestions = [spot['Name'] for spot in foodspots]

        return jsonify(suggestions), 200
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
            SELECT 
                fs.Id AS FoodSpotId, 
                fs.Name, 
                fs.Rating, 
                fs.ImageUrl, 
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
            LEFT JOIN favorites f 
                ON fs.Id = f.FoodSpotId 
                AND f.CustomerId = (
                    SELECT Id 
                    FROM customer 
                    WHERE UserId = %s
                )
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

@app.route('/add_foodspot', methods=['POST'])
@token_required
def add_foodspot():
    user_id = extract_user_id_from_token()
    
    # Check if the user is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can add a food spot.'}), 403

    data = request.json
    admin_id = user_id  # Use user_id as the admin adding the food spot
    name = data['name']
    address = data['address']
    image_url = data['imageUrl']
    phone_number = data['phoneNumber']
    opening_time = data['openingTime']
    closing_time = data['closingTime']
    rating = data.get('rating', 0)  # Default to 0 if no rating is provided

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into FoodSpot table
        foodspot_query = """
            INSERT INTO foodspot (AdminId, Name, Address, ImageUrl, PhoneNumber, OpeningTime, ClosingTime, Rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(foodspot_query, (admin_id, name, address, image_url, phone_number, opening_time, closing_time, rating))
        conn.commit()

        return jsonify({'message': 'FoodSpot added successfully'}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/update_foodspot/<foodspot_id>', methods=['PUT'])
@token_required
def update_foodspot(foodspot_id):
    user_id = extract_user_id_from_token()
    
    # Check if the user is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can update a food spot.'}), 403

    data = request.json
    name = data.get('name')
    address = data.get('address')
    image_url = data.get('imageUrl')
    phone_number = data.get('phoneNumber')
    opening_time = data.get('openingTime')
    closing_time = data.get('closingTime')
    rating = data.get('rating')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Build update query dynamically based on provided fields
        update_query = "UPDATE foodspot SET "
        fields = []
        values = []

        if name:
            fields.append("Name = %s")
            values.append(name)
        if address:
            fields.append("Address = %s")
            values.append(address)
        if image_url:
            fields.append("ImageUrl = %s")
            values.append(image_url)
        if phone_number:
            fields.append("PhoneNumber = %s")
            values.append(phone_number)
        if opening_time:
            fields.append("OpeningTime = %s")
            values.append(opening_time)
        if closing_time:
            fields.append("ClosingTime = %s")
            values.append(closing_time)
        if rating is not None:
            fields.append("Rating = %s")
            values.append(rating)

        update_query += ", ".join(fields) + " WHERE Id = %s"
        values.append(foodspot_id)

        cursor.execute(update_query, tuple(values))
        conn.commit()

        return jsonify({'message': 'FoodSpot updated successfully'}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_foodspot/<foodspot_id>', methods=['DELETE'])
@token_required
def delete_foodspot(foodspot_id):
    user_id = extract_user_id_from_token()
    
    # Check if the user is an admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized. Only admins can delete a food spot.'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        delete_query = "DELETE FROM foodspot WHERE Id = %s"
        cursor.execute(delete_query, (foodspot_id,))
        conn.commit()

        return jsonify({'message': 'FoodSpot deleted successfully'}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/is_admin', methods=['GET'])
@token_required
def check_if_admin():
    # Extract userId from the token
    user_id = extract_user_id_from_token()

    try:
        # Use the utility function to check admin status
        is_admin_status = is_admin(user_id)

        return jsonify({'isAdmin': is_admin_status}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/logs/error', methods=['GET'])
def get_parsed_error_log():
    try:
        parsed_logs = parse_error_log(ERROR_LOG_FILE_PATH)
        return jsonify(parsed_logs), 200
    except FileNotFoundError:
        return jsonify({'error': f'Log file not found: {ERROR_LOG_FILE_PATH}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs/error/download', methods=['GET'])
def download_error_log():
    try:
        return send_file(ERROR_LOG_FILE_PATH, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': f'Log file not found: {ERROR_LOG_FILE_PATH}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs/access', methods=['GET'])
def get_parsed_access_log():
    try:
        parsed_logs = parse_access_log(ACCESS_LOG_FILE_PATH)
        return jsonify(parsed_logs), 200
    except FileNotFoundError:
        return jsonify({'error': 'Access log file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs/access/download', methods=['GET'])
def download_access_log():
    try:
        return send_file(ACCESS_LOG_FILE_PATH, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Access log file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to get geolocation data from ipinfo.io
def get_geo_location(ip_address):
    try:
        api_url = f"https://ipinfo.io/{ip_address}?token=169b1821a29c6d"
        response = requests.get(api_url)
        if response.status_code == 200:
            print(response)
            return response.json() 
        else:
            return None
    except Exception as e:
        print(f"Error fetching geolocation: {e}")
        return None

# Endpoint to get location details
@app.route('/get_location', methods=['GET'])
def get_location():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(ip)
    
    if not ip:
        return jsonify({'error': 'Unable to determine IP address'}), 400
    
    # Fetch geolocation data
    geo_data = get_geo_location(ip)
    print(geo_data)
    if geo_data:
        latitude, longitude = geo_data['loc'].split(',')
        return jsonify({
            'ip': ip,
            'latitude': latitude,
            'longitude': longitude,
            'city': geo_data.get('city', 'Unknown'),
            'region': geo_data.get('region', 'Unknown'),
            'country': geo_data.get('country', 'Unknown')
        })
    else:
        return jsonify({'error': 'Failed to fetch geolocation data'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8024, debug=True)