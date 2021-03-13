class Permission:
  def denied():
    return {'message': 'Permission denied.'}, 401