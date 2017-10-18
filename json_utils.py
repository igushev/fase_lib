import copy
import datetime
import json
import os

    
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = '%s %s' % (DATE_FORMAT, TIME_FORMAT)
MODULE_FIELD = '__module__'
CLASS_FIELD = '__class__'


class JSONObjectInterface(object):
  
  def ToSimple(self, obj):
    raise NotImplemented()
  
  def FromSimple(self, simple):
    raise NotImplemented()


class JSONString(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, (str, unicode))
    return obj
  
  def FromSimple(self, simple):
    assert isinstance(simple, (str, unicode))
    return simple


class JSONFloat(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, float)
    return obj
  
  def FromSimple(self, simple):
    assert isinstance(simple, (float, int))
    return float(simple)


class JSONInt(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, int)
    return obj
  
  def FromSimple(self, simple):
    assert isinstance(simple, int)
    return simple


class JSONBool(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, bool)
    return obj

  def FromSimple(self, simple):
    assert isinstance(simple, (bool, int))
    return bool(simple)


class JSONDate(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, datetime.date)
    return obj.strftime(DATE_FORMAT)
  
  def FromSimple(self, simple):
    assert isinstance(simple, basestring)
    return datetime.datetime.strptime(simple, DATE_FORMAT).date()


class JSONDateTime(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, datetime.datetime)
    return obj.strftime(DATETIME_FORMAT)
  
  def FromSimple(self, simple):
    assert isinstance(simple, basestring)
    return datetime.datetime.strptime(simple, DATETIME_FORMAT)


class JSONObject(JSONObjectInterface):
  
  def __init__(self, cls):
    self._cls = cls

  def ToSimple(self, obj):
    return obj.ToSimple()
  
  def FromSimple(self, simple):
    return self._cls.FromSimple(simple)

  
class JSONList(object):
  
  def __init__(self, json_obj):
    assert isinstance(json_obj, JSONObjectInterface)
    self._json_obj = json_obj
    
  def ToSimple(self, obj):
    assert isinstance(obj, list)
    return [self._json_obj.ToSimple(item) for item in obj]
  
  def FromSimple(self, simple):
    assert isinstance(simple, list)
    return [self._json_obj.FromSimple(item) for item in simple]


class JSONDict(object):
  
  def __init__(self, key_json_obj, value_json_obj):
    assert isinstance(key_json_obj, JSONObjectInterface)
    assert isinstance(value_json_obj, JSONObjectInterface)
    self._key_json_obj = key_json_obj
    self._value_json_obj = value_json_obj
  
  def ToSimple(self, obj):
    assert isinstance(obj, dict)
    return {self._key_json_obj.ToSimple(key):
            self._value_json_obj.ToSimple(value)
            for key, value in obj.iteritems()}
  
  def FromSimple(self, simple):
    assert isinstance(simple, dict)
    return {self._key_json_obj.FromSimple(key):
            self._value_json_obj.FromSimple(value)
            for key, value in simple.iteritems()}


def ToSimple(self):
  obj_cls = self.__class__
  simple = dict()
  for key, value in self.__dict__.iteritems():
    json_obj = obj_cls.desc_dict[key]
    simple[key] = json_obj.ToSimple(value) if value is not None else None
  for key, json_obj in obj_cls.desc_dict.iteritems():
    if key in self.__dict__:
      continue
    simple[key] = None
  if obj_cls.inherited:
    simple[MODULE_FIELD] = obj_cls.__module__
    simple[CLASS_FIELD] = obj_cls.__name__
  return simple


def ToJSON(self):
  return json.dumps(self.ToSimple())


@classmethod
def FromSimple(cls, simple):
  if cls.inherited:
    obj_cls = getattr(os.sys.modules[simple[MODULE_FIELD]], simple[CLASS_FIELD])
  else:
    obj_cls = cls

  obj_dict = dict()
  for key, value in simple.iteritems():
    if key in [MODULE_FIELD, CLASS_FIELD]:
      continue
    json_obj =  obj_cls.desc_dict[key]
    obj_dict[str(key)] = (json_obj.FromSimple(value)
                          if value is not None else None)
  for key, json_obj in obj_cls.desc_dict.iteritems():
    if key in simple:
      continue
    obj_dict[key] = None
  obj = obj_cls.__new__(obj_cls)
  obj.__dict__ = obj_dict 
  return obj


@classmethod
def FromJSON(cls, data):
  return cls.FromSimple(json.loads(data))


class JSONDecorator(object):
  
  def __init__(self, desc_dict=None, inherited=False):
    self.desc_dict = desc_dict or {}
    self.inherited = inherited

  def __call__(self, cls):
    desc_dict = copy.copy(self.desc_dict)
    inherited = self.inherited

    cls_queue = [cls]
    cls_visited = set([])
    while len(cls_queue):
        curr_cls = cls_queue.pop(0)
        for base in curr_cls.__bases__:
          if getattr(base, 'desc_dict', None) is None:
            continue
          if base in cls_visited:
            continue
          cls_visited.add(base)
          desc_dict.update(base.desc_dict)
          inherited = inherited or base.inherited
          cls_queue.append(base)
    
    cls.desc_dict = desc_dict
    cls.inherited = inherited
    cls.ToSimple = ToSimple
    cls.ToJSON = ToJSON
    cls.FromSimple = FromSimple
    cls.FromJSON = FromJSON
    return cls
