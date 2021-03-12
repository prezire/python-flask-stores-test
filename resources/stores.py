from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from models.stores import Store as StoreModel

class Store(Resource):
  
  @staticmethod
  def __exists(name:str) -> bool:
    return StoreModel.find_by_name(name) is not None
    
  @staticmethod
  def __show_exists_err(name:str):
    return {'message': f'The store {name} already exists.'}, 302
  
  @staticmethod
  def __uid() -> int:
    return current_identity.id
  
  @staticmethod
  def __name_arg():
    p = reqparse.RequestParser()
    p.add_argument('name', required=True)
    return p.parse_args()['name']
  
  @jwt_required()
  def get(self):
    store = StoreModel.find_by_name(self.__name_arg())
    if store:
      store = store.json()
    return {'store': store}, 200 if store else 404
  
  @jwt_required()
  def post(self):
    name = self.__name_arg()
    if Store.__exists(name):
      return Store.__show_exists_err(name)
    return {'store': StoreModel(name, Store.__uid()).save().json()}
  
  @jwt_required()
  def put(self):
    p = reqparse.RequestParser()
    p.add_argument('old_name', required=True)
    p.add_argument('new_name', required=True)
    args = p.parse_args()
    old_name = args['old_name']
    new_name = args['new_name']
    if Store.__exists(new_name):
      return Store.__show_exists_err(new_name)
    store = StoreModel.find_by_name(old_name)
    stat = 'created'
    if store:
      store.name = new_name
      stat = 'updated'
    else:
      store = StoreModel(old_name, Store.__uid())
    store.save()
    return {stat: store.json()}
  
  @jwt_required()
  def delete(self):
    store = StoreModel.find_by_name(self.__name_arg())
    if store:
      return {'deleted': store.delete()}
    return {'message': 'No stores to delete.'}, 404

class StoreList(Resource):
  @jwt_required()
  def get(self):
    return {'stores': [s.json() for s in StoreModel.all()]}