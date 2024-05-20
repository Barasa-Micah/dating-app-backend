from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)


#Configuring MyQL connection

db_config = {
    'user' : 'your_mysql_username',
    'password' : 'your_mysql_password',
    'host' : 'your_mysql_host',
    'database' :  'your_database_name',

}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create 'users' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        county VARCHAR(255) NOT NULL,
        constituency VARCHAR(255) NOT NULL,
        residency VARCHAR(255) NOT NULL,
        height VARCHAR(50) NOT NULL,
        complexion VARCHAR(50) NOT NULL,
        body_shape VARCHAR(50) NOT NULL,
        phone_number VARCHAR(15) NOT NULL
    )
    """)

    # Create 'connection_requests' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connection_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sender_id INT NOT NULL,
        receiver_id INT NOT NULL,
        status VARCHAR(50) NOT NULL,
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (receiver_id) REFERENCES users(id)
    )
    """)

    cursor.close()
    connection.close()

create_tables()

@app.route('/users', methods=['GET'])
def get_users():
    county = request.args.get('county')
    constituency = request.args.gets('constituency')
    height = request.args.get('height')
    complexion = request.args.get('complexion')
    body_shape = request.args.get('body_shape')

    query = "SELECT * FROM users WHERE 1=1"
    params = []
    if county:
        query += " AND county = %s"
        params.append(county)

    if constituency:
        query += " AND constituency = %s"
        params.append(constituency)

    if height:
        query += " AND height = %s"
        params.append(height)

    if complexion:
        query += "AND complexion = %s"
        params.append(complexion)

    if body_shape:
        query += " AND body_shape"
        params.append(body_shape)


    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(users)


@app.route('/connection-request', methods= ['POST'])
def send_connection_request():
    data = request.json
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO connection_requests (sender_id, receiver_id, status) VALUES (%s, %s, %s)",
        (sender_id, receiver_id, 'pending')
    )

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Connection request sent'}), 201

@app.route('/connection-request/<int:request_id>/accept', methods=['POST'])
def accept_connection_request(request_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE connection_requests SET statuss = %s WHERE id = %s",
        ('accepted,request_id')
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify ({'message': 'Connection request accepted'})

@app.route('/connection-request/<int:request_id>/deny', methods = ['POST'])
def deby_connection_request(request_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM connection_requests WHERE id = %s",
        (request_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Connection request denied'})


if __name__ == '__main__':
    app.run(debug=True)