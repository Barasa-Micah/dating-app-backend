from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL


app = Flask(__name__)
CORS(app)

#MySQL configurations

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'micacodes'
app.config['MYSQL_PASSWORD'] = 'mica'
app.config['MYSQL_DB'] ='datingApp'

mysql =MySQL(app)


from routes.user_routes import user_bp
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True, port=5000)