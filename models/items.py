from .dbs import db

class Item(db.Model):
  __tablename__ = 'items'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  price = db.Column(db.Float(precision=2))
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=True)
  store = db.relationship('Store')
  
  def __init__(self, name:str, price:float, store_id:int):
    self.name = name
    self.price = price
    self.store_id = store_id
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return self.find_by_name(self.name)
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
    
  @classmethod
  def all(cls):
    return cls.query.all()
    
  @classmethod
  def find_by_name(cls, name:str):
    return cls.query.filter_by(name=name).first()
    
  def json(self):
    s = self.store
    store = None
    if s:
      store = {'id': s.id, 'name': s.name}
    return {'id': self.id, 'name': self.name, 'price': self.price, 'store': store}