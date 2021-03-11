from flask_restful import Resource, reqparse
from models.users import User
    
class Register(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)
    data = parser.parse_args()
    username = data['username']
    if User.find_by_username(username):
      return {'message': 'User already exists'}, 400
    user = User(username, data['password']).save()
    return {'success': True, 'user': user.json()}