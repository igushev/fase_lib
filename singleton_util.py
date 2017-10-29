@classmethod
def Set(cls, instance, overwrite=False):
  assert cls._instance is None or overwrite is True
  assert isinstance(instance, cls)
  cls._instance = instance


@classmethod
def Get(cls):
  assert cls._instance is not None
  return cls._instance


class Singleton(object):

  def __init__(self):
    pass

  def __call__(self, cls):
    cls._instance = None
    cls.Set = Set
    cls.Get = Get
    return cls
