import inspect
import os
import sys
import re

from base_util import data_util
from base_util import json_util


FIELD_DESC_REGEXP = '.*\'(?P<field_name>[a-zA-Z0-9_]+)\'\:\ ?json_util\.JSON.*'
CLASS_DEF_REGEXP = 'class (?P<class_name>[a-zA-z0-9]+)\([a-zA-z0-9\.]+\)\:'
CONSTANT_DEF_REGEXP = '\ +(?P<name>[A-Z_]+)\ ?=\ ?(?P<value>.+)'


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
  cls_field_names_dict = {}
  field_names = []
  first_class = True
  with open(filepath, 'w') as spec_file:
    spec_file.write('# Put Your Header Here\n')
    for line in inspect.getsource(module).split('\n'):
      constant_def_match = re.match(CONSTANT_DEF_REGEXP, line)
      if constant_def_match:
        spec_file.write('    * %s = %s\n' % (constant_def_match.group('name'), constant_def_match.group('value')))
      field_desc_match = re.match(FIELD_DESC_REGEXP, line)
      if field_desc_match:
        field_names.append(field_desc_match.group('field_name'))

      class_def_match = re.match(CLASS_DEF_REGEXP, line)
      if not class_def_match:
        continue
      cls_name = class_def_match.group('class_name')
      cls = cls_dict[cls_name]
      if not issubclass(cls, data_util.AbstractObject):
        continue
      if cls == data_util.AbstractObject:
        continue
      if not first_class:
        spec_file.write('\n')
      spec_file.write('* **%s**' % cls_name)

      base_names = [base.__name__ for base in cls.__bases__ if base is not data_util.AbstractObject]
      for base_name in base_names:
        field_names = cls_field_names_dict[base_name] + field_names
      if base_names:
        spec_file.write(' extends *%s*' % ', '.join(base_names))
      if cls.__doc__:
        spec_file.write('. %s' % cls.__doc__)
      spec_file.write('\n')

      assert set(field_names) == set(cls.desc_dict.keys()), (cls_name, set(field_names), set(cls.desc_dict.keys())) 
      assert len(field_names) == len(set(field_names))
      for arg_name in field_names:
        json_obj = cls.desc_dict[arg_name]
        arg_type = JSONObjectStr(json_obj)
        spec_file.write('  * *%s*: %s\n' % (arg_name, arg_type))

      cls_field_names_dict[cls_name] = field_names[:]
      field_names.clear()
      first_class = False


def main(argv):
  assert len(argv) == 3
  module_name = argv[1]
  filepath = argv[2]  
  GenerateDataSpecification(module_name, filepath)


if __name__ == '__main__':
  main(os.sys.argv)
