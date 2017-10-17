class Device(object):
  pass

class User(object):
  pass

class BadRequest(object):

  def __init__(self, code, message):
    self.code = code
    self.message = message