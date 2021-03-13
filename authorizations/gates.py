from flask_jwt_extended import get_current_user

class Delete:
  @classmethod
  def can(cls):
    return get_current_user()['payload']['sub'] == 1