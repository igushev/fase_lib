import inspect
import os
import sys
import re

from base_util import data_util
from json_util import json_util

CLASS_DEF_REGEXP = 'class (?P<class_name>[a-zA-z0-9]+)\([a-zA-z0-9\.]+\)\:'


def JSONObjectStr(json_obj):
  if isinstance(json_obj, json_util.JSONString):
    return 'string'
  elif isinstance(json_obj, json_util.JSONFloat):
    return 'float'
  elif isinstance(json_obj, json_util.JSONInt):
    return 'int'
  elif isinstance(json_obj, json_util.JSONBool):
    return 'bool'
  elif isinstance(json_obj, json_util.JSONDateTime):
    return 'date'
  elif isinstance(json_obj, json_util.JSONDateTime):
    return 'datetime'
  elif isinstance(json_obj, json_util.JSONFunction):
    return 'function'
  elif isinstance(json_obj, json_util.JSONObject):
    cls_name = '*%s*' % json_obj._cls.__name__
    if json_obj._cls.inherited:
      cls_name += ' or subclass'
    return cls_name
  elif isinstance(json_obj, json_util.JSONTuple):
    return 'tuple(%s)' % ', '.join(JSONObjectStr(json_obj) for json_obj in json_obj._json_obj_list)
  elif isinstance(json_obj, json_util.JSONList):
    return 'list(%s)' % JSONObjectStr(json_obj._json_obj)
  elif isinstance(json_obj, json_util.JSONDict):
    return 'dict(%s->%s)' % (JSONObjectStr(json_obj._key_json_obj),
                             JSONObjectStr(json_obj._value_json_obj))
  else:
    raise AssertionError('Unknown JSONObjectInterface: %s' %
                         json_obj.__class__.__name__)
  

def GenerateDataSpecification(module_name, filepath):
  exec('import %s' % module_name)
  module = sys.modules[module_name]
  cls_dict = {cls_name: cls for cls_name, cls in inspect.getmembers(module, inspect.isclass)}

  with open(filepath, 'w') as spec_file:
    spec_file.write('# Put Your Header Here\n')
    for line in inspect.getsource(module).split('\n'):
      class_def_match = re.match(CLASS_DEF_REGEXP, line)
      if not class_def_match:
        continue
      cls_name = class_def_match.group('class_name')
      cls = cls_dict[cls_name]
      if not issubclass(cls, data_util.AbstractObject):
        continue
      if cls == data_util.AbstractObject:
        continue
      spec_file.write('* **%s**' % cls_name)
      
      bases_names = [base.__name__ for base in cls.__bases__ if base is not  data_util.AbstractObject]
      if bases_names:
        spec_file.write(' extends *%s*' % ', '.join(bases_names))
      spec_file.write('\n')

      for arg_name, json_obj in cls.desc_dict.items():
        arg_type = JSONObjectStr(json_obj)
        spec_file.write('  * *%s*: %s\n' % (arg_name, arg_type))

      spec_file.write('\n')


def main(argv):
  assert len(argv) == 3
  module_name = argv[1]
  filepath = argv[2]  
  GenerateDataSpecification(module_name, filepath)


if __name__ == '__main__':
  main(os.sys.argv)
