import hashlib


def HashKey(obj):
  if hasattr(obj, 'HashKey'):
    return obj.HashKey()
  elif hasattr(obj, '__dict__'):
    return HashKey(obj.__dict__)
  elif isinstance(obj, (list, tuple)):
    m = hashlib.md5()
    for item in obj:
      m.update(HashKey(item))
    return m.hexdigest()
  elif isinstance(obj, set):
    m = hashlib.md5()
    for item in sorted(obj):
      m.update(HashKey(item))
    return m.hexdigest()
  elif isinstance(obj, dict):
    m = hashlib.md5()
    for key, value in sorted(obj.iteritems()):
      m.update(HashKey(key))
      m.update(HashKey(value))
    return m.hexdigest()
  else:
    m = hashlib.md5()
    m.update(repr(obj).encode('utf-8'))
    return m.hexdigest()


class AbstractObject(object):

  def __str__(self):
    return '\n'.join(['%s: %s' % (key, value)
                      for key, value in sorted(self.__dict__.iteritems())])

  def __repr__(self):
    return str(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def HashKey(self):
    return HashKey(self.__dict__)
