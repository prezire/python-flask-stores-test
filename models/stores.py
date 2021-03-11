from .dbs import db

class Store(db.Model):
  __tablename__ = 'stores'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  items = db.relationship('Item', lazy='dynamic')
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
  user = db.relationship('User')
  
  def __init__(self, name:str, user_id:int):
    self.name = name
    self.user_id = user_id
    
  @classmethod
  def all(cls):
    return cls.query.all()
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return Store.find_by_name(self.name)
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
    
  @classmethod
  def find(cls, id:int):
    return cls.query.filter_by(id=id).first()
    
  @classmethod
  def find_by_name(cls, name:str):
    return cls.query.filter_by(name=name).first()
  
  def json(self):
    i = self.items
    items = None
    if i:
      items = [item.json() for item in i.all()]
    u = self.user
    user = {'id': u.id, 'username': u.username}
    return {'id': self.id, 'name': self.name, 'items': items, 'owner': user}