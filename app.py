from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from securities import auth, identity
from resources.users import Register as UserRegister
from resources.items import Item, ItemList
from resources.stores import Store, StoreList
from datetime import timedelta
from models.dbs import db

app = Flask(__name__)
app.secret_key = 'test'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
jwt = JWT(app, auth, identity)

db.init_app(app)
db.app = app

#Heroku.
#application = app

if __name__ == '__main__':
  @app.before_first_request
  def migrate():
    db.create_all()
    
  @app.route('/')
  def home():
    return render_template('index.html')
  
  def main():
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    
    api.add_resource(Store, '/store')
    api.add_resource(StoreList, '/stores')
    
    api.add_resource(UserRegister, '/register')
    app.run(debug=True)
    
  main()