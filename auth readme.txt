from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models import User


# parse & validate the incoming JSON
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('email', type=str, required=True, help='Email is required')
signup_parser.add_argument('password', type=str, required=True, help='Password is required')

# parser for login
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

class Signup(Resource):
    def post(self):
        args = signup_parser.parse_args()
        # check for existing user
        if User.query.filter_by(email=args['email']).first():
            return {'message': 'Email already registered'}, 400

        # create & save new user
        user = User(
            email=args['email'],
            password_hash=generate_password_hash(args['password'])
        )
        db.session.add(user)
        db.session.commit()

        return {'id': user.id, 'email': user.email}, 201
    
class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if not user or not check_password_hash(user.password_hash, args['password']):
            return {'message': 'Invalid credentials'}, 401

        token = create_access_token(identity=user.id)
        return {'access_token': token}, 200