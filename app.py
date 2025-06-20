from flask import Flask
from extensions import db, migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.auth import Signup, Login

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'a-very-secret-key' 


db.init_app(app)
migrate.init_app(app, db)
import models
jwt = JWTManager(app)

api = Api(app)
api.add_resource(Signup, '/api/auth/signup')
api.add_resource(Login,  '/api/auth/login', '/api/auth/login/')


@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    print(app.url_map)  
    app.run(port=5000, debug=True, use_reloader=False)

