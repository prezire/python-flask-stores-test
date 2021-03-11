from .dbs import db

class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100))
  password = db.Column(db.String(100))
  stores = db.relationship('Store', lazy=True)
  
  def __init__(self, username:str, password:str):
    self.username = username
    self.password = password
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return self.find_by_id(self.id)
    
  @classmethod
  def find_by_username(cls, username:str):
    return cls.query.filter_by(username=username).first()
    
  @classmethod
  def find_by_id(cls, id:int):
    return cls.query.filter_by(id=id).first()
    
  def json(self):
    s = self.stores
    stores = None
    if s:
      stores = [s.json() for s in s.all()]
    return {'id': self.id, 'username': self.username, 'stores': stores}