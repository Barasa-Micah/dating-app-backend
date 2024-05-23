from flask import jsonify, request
from app import mysql


def get_users():
    county = request.args.get('county')
    constituency = request.args.get('constituency')
    height = request.args.get('height')
    complexion = request.args.get('complexion')
    body_shape = request.args.get('body_shape')
    hairstyle = request.args.get('hairstyle')
    beards = request.args.get('beards')


    query = "SELECT * FROM users WHERE 1=1"
    filters = []

    if county:
        query += " AND county =%s"
        filters.appemd(county)

    if constituency:
        query += " AND constituency = %s"
        filters.append(constituency)

    if height:
        query += " AND height = %s"
        filters.append(height)

    if complexion:
        query += " AND complexion =%s"
        filters.append(complexion)

    if body_shape:
        query += " AND body_shape %s"
        filters.append(body_shape)

    if hairstyle:
        query += " AND hairstyle %s"
        filters.append(hairstyle)


    if beards:
        query += "AND beards %s"
        filters.append(beards == 'true')

    cursor = mysql.connection.cursor()
    cursor.execute(query, tuple(filters))
    results = cursor.fetchall()
    cursor.close()

    users = []
    for row in results:
        user = {
            'id': row[0],
            'name': row[1],
            'county': row[2],
            'constituency': row[3],
            'height': row[4],
            'complexion': row[5],
            'body_shape': row[6],
            'hairstyle': row[7],
            'beards': row[8],
            'phone_number': row[9],
            'connections': row[10],
            'connection_requests': row[11],
        }
        users.append(user)

    return jsonify(users)

def send_connection_request():
    data = request.get_json()
    user_id = data['userId']
    target_user_id = data['targetUserId']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT connection_requests FROM users WHERE id = %s", (target_user_id,))
    result = cursor.fetchone()
    connection_requests = result[0] if result[0] else []
    connection_requests.append(user_id)

    cursor.execute("UPDATE users SET connection_requests = %s WHERE id = %s", (connection_requests, target_user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Connection request sent'})

def accept_connection_request():
    data = request.get_json()
    user_id = data['userId']
    target_user_id = data['targetUserId']

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT connections, connection_requests FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    connections = result[0] if result[0] else []
    connection_requests = result[1] if result[1] else []
    connections.append(target_user_id)
    connection_requests.remove(target_user_id)

    cursor.execute("UPDATE users SET connections = %s, connection_requests = %s WHERE id = %s", (connections, connection_requests, user_id))

    cursor.execute("SELECT connections FROM users WHERE id = %s", (target_user_id,))
    result = cursor.fetchone()
    target_connections = result[0] if result[0] else []
    target_connections.append(user_id)

    cursor.execute("UPDATE users SET connections = %s WHERE id = %s", (target_connections, target_user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Connection request accepted'})

def deny_connection_request():
    data = request.get_json()
    user_id = data['userId']
    target_user_id = data['targetUserId']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT connection_requests FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    connection_requests = result[0] if result[0] else []
    connection_requests.remove(target_user_id)

    cursor.execute("UPDATE users SET connection_requests = %s WHERE id = %s", (connection_requests, user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Connection request denied'})