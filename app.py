import os
from flask import Flask, render_template, url_for, jsonify, request
from flask_restful import Api
from flask_jwt import JWT
from securities import auth, identity
from resources.users import Register as UserRegister
from resources.items import Item, ItemList
from resources.stores import Store, StoreList
from datetime import timedelta
from models.dbs import db
import stripe

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'test')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///flask.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Stripe.
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_e8DCmlbNAsG1Weums7EojPmT'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_b8YylRQAEPjzU8GVI2EDQgZG'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

api = Api(app)
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.init_app(app)

jwt = JWT(app, auth, identity)

db.init_app(app)

@app.before_first_request
def migrate():
  db.create_all()
  
#TODO: Move to BluePrint.
@app.route('/')
def home():
  return render_template('index.html', title='Home')
  
@app.route('/shop')
def shop():
  return render_template('shop.html', title='Shopping')
  
#TODO: Move to Resource.
@app.route('/checkout', methods=['POST'])
def checkout():
  items = [{
    'price': 'price_1ITnsCLq4iF64WhR5pR4U8er',
    'quantity': 1,
  }]
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=items,
    mode='payment',
    success_url=url_for('thank_you', _external=True),
    cancel_url=url_for('shop', _external=True),
  )
  return jsonify(
    session_id=session.id, 
    checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
  )
  
@app.route('/thank-you')
def thank_you():
  return render_template('thank_you.html', title='Thank You')

if __name__ == '__main__':
  app.run(debug=True)