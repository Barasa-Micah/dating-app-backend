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