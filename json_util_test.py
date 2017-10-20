import unittest
import datetime

from Yusi.YuUtils.hash_utils import HashKey
from Yusi.YuUtils.repr_utils import Repr

import json_util


@json_util.JSONDecorator(
    {'_int_field': json_util.JSONInt(),
     'float_field': json_util.JSONFloat(),
     '_string_field': json_util.JSONString(),
     'date_field': json_util.JSONDate(),
     'datetime_field': json_util.JSONDateTime()})
class WithFields(object):
  
  def __init__(self, int_field, float_field, string_field, date_field,
               datetime_field):
    assert isinstance(int_field, int)
    assert isinstance(float_field, float)
    assert isinstance(string_field, basestring)
    assert isinstance(date_field, datetime.date)
    assert isinstance(datetime_field, datetime.datetime)
    self._int_field = int_field  # With underscore.
    self.float_field = float_field
    self._string_field = string_field  # With underscore.
    self.date_field = date_field
    self.datetime_field = datetime_field

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'nested_list': json_util.JSONList(json_util.JSONObject(WithFields)),
     'nest_dict': json_util.JSONDict(json_util.JSONString(),
                                      json_util.JSONObject(WithFields))})
class WithListAndDict(object):
  
  def __init__(self, nested_list, nest_dict):
    assert isinstance(nested_list, list)
    assert isinstance(nest_dict, dict)
    self.nested_list = nested_list
    self.nest_dict = nest_dict

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'_nested_with_fields': json_util.JSONObject(WithFields),
     '_nested_with_list_and_dict': json_util.JSONObject(WithListAndDict),
     '_none_value': json_util.JSONString(),
     '_bool_value': json_util.JSONBool()})
class WithNestedFields(object):

  def __init__(self, nested_with_fields, nested_with_list_and_dict,
               none_value, bool_value):
    assert isinstance(nested_with_fields, WithFields)
    assert isinstance(nested_with_list_and_dict, WithListAndDict)
    # With underscore.
    self._nested_with_fields = nested_with_fields
    # With underscore.
    self._nested_with_list_and_dict = nested_with_list_and_dict
    self._none_value = none_value
    self._bool_value = bool_value

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


# We declare _nested_with_fields_2 to be WithFields but allow None.
@json_util.JSONDecorator(
    {'_nested_with_fields_1': json_util.JSONObject(WithFields),
     '_nested_with_fields_2': json_util.JSONObject(WithFields)})
class WithNestedNoneObjectsFields(object):

  def __init__(self, nested_with_fields_1, nested_with_fields_2):
    assert isinstance(nested_with_fields_1, WithFields)
    if nested_with_fields_2 is not None:
      assert isinstance(nested_with_fields_2, WithFields)
    # With underscore.
    self._nested_with_fields_1 = nested_with_fields_1
    # With underscore.
    self._nested_with_fields_2 = nested_with_fields_2

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var1': json_util.JSONFloat()},
    inherited=True)
class Level1(object):

  def __init__(self, var1):
    assert isinstance(var1, float)
    self.var1 = var1

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var2': json_util.JSONFloat()})
class Level2(Level1):

  def __init__(self, var1, var2):
    super(Level2, self).__init__(var1)
    assert isinstance(var2, float)
    self.var2 = var2

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var3': json_util.JSONFloat()})
class Level3A(Level2):

  def __init__(self, var1, var2, var3):
    super(Level3A, self).__init__(var1, var2)
    assert isinstance(var3, float)
    self.var3 = var3

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var3': json_util.JSONString()})
class Level3B(Level2):

  def __init__(self, var1, var2, var3):
    super(Level3B, self).__init__(var1, var2)
    assert isinstance(var3, basestring)
    self.var3 = var3

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'diff_level_list': json_util.JSONList(json_util.JSONObject(Level1))})
class WithDifferentLevelList(object):
  
  def __init__(self, diff_level_list):
    assert isinstance(diff_level_list, list)
    self.diff_level_list = diff_level_list

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__



@json_util.JSONDecorator(
    {'var1': json_util.JSONString(),
     'var2': json_util.JSONString(),
     'var3': json_util.JSONString()})
class StateNotFull(object):
  
  def __init__(self, var1, var2):
    self.var1 = var1
    self.var2 = var2

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var1': json_util.JSONFloat()},
    inherited=True)
class Base1(object):

  def __init__(self, var1):
    assert isinstance(var1, float)
    self.var1 = var1

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var2': json_util.JSONFloat()},
    inherited=True)
class Base2(object):

  def __init__(self, var2):
    assert isinstance(var2, float)
    self.var2 = var2

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var3': json_util.JSONFloat()},
    inherited=True)
class Base1_2(Base1, Base2):

  def __init__(self, var1, var2, var3):
    Base1.__init__(self, var1)
    Base2.__init__(self, var2)
    assert isinstance(var3, float)
    self.var3 = var3

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_util.JSONDecorator(
    {'var4': json_util.JSONFloat()},
    inherited=True)
class Derived(Base1_2):

  def __init__(self, var1, var2, var3, var4):
    Base1_2.__init__(self, var1, var2, var3)
    assert isinstance(var4, float)
    self.var4 = var4

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class ClassWithMethod(object):

  def __init__(self, var1):
    self.var1 = var1

  def Method(self, var2):
    return self.var1 + var2


@json_util.JSONDecorator(
    {'method': json_util.JSONClassMethod()})
class WithClassMethod(object):
  
  def __init__(self, method):
    self.method = method

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class JSONUtilsTest(unittest.TestCase):

  def AssertToFrom(self, obj, obj_cls):
    obj_simple = obj.ToSimple()
    obj_from_simple = obj_cls.FromSimple(obj_simple)
    self.assertEqual(obj.HashKey(), obj_from_simple.HashKey())
    self.assertEqual(repr(obj), repr(obj_from_simple))
    self.assertEqual(obj, obj_from_simple)
    
    obj_json = obj.ToJSON()
    obj_from_json = obj_cls.FromJSON(obj_json)
    self.assertEqual(obj.HashKey(), obj_from_json.HashKey())
    self.assertEqual(repr(obj), repr(obj_from_json))
    self.assertEqual(obj, obj_from_json)

  def testGeneral(self):
    date_1 = datetime.date(1986, 5, 22)
    date_2 = datetime.date(1986, 8, 21)
    date_3 = datetime.date(2014, 1, 3)
    datetime_1 = datetime.datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime.datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime.datetime(2014, 1, 3, 9, 54, 0)
    obj = WithNestedFields(
        WithFields(3, 5., u'seven', date_1, datetime_1),
        WithListAndDict(
            [WithFields(2, 4., u'six', date_2, datetime_2),
             WithFields(8, 10., u'twelve', date_2, datetime_2)],
            {u'one': WithFields(15, 17., u'nineteen', date_3, datetime_3),
             u'two': WithFields(21, 23., u'twenty five', date_3, datetime_3)}),
        None, True)
    self.AssertToFrom(obj, WithNestedFields)

  def testInheritance(self):
    level3a = Level3A(1., 3., 5.)
    self.AssertToFrom(level3a, Level3A)
    # Can call using parent class.
    self.AssertToFrom(level3a, Level1)
    level3b = Level3B(2., 4., u'six')
    self.AssertToFrom(level3b, Level3B)
    # Can call using parent class.
    self.AssertToFrom(level3b, Level1)

    # List of mixed instances of derivative classes.    
    level3a_2 = Level3A(7., 9., 11.)
    level3b_2 = Level3B(8., 10., u'twelve')
    obj = WithDifferentLevelList(
        [level3a, level3b, level3a_2, level3b_2])
    self.AssertToFrom(obj, WithDifferentLevelList)

  def testNestedObjectNone(self):
    date_1 = datetime.date(1986, 5, 22)
    date_2 = datetime.date(1986, 8, 21)
    date_3 = datetime.date(2014, 1, 3)
    datetime_1 = datetime.datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime.datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime.datetime(2014, 1, 3, 9, 54, 0)
    # Both fields are set.
    obj = WithNestedNoneObjectsFields(
        WithFields(3, 5., u'seven', date_1, datetime_1),
        WithFields(2, 4., u'six', date_2, datetime_2))
    self.AssertToFrom(obj, WithNestedNoneObjectsFields)

    # Second field is None.
    obj = WithNestedNoneObjectsFields(
        WithFields(15, 17., u'nineteen', date_3, datetime_3), None)
    self.AssertToFrom(obj, WithNestedNoneObjectsFields)

  def testStateFull(self):
    state_not_full = StateNotFull(u'one', u'two')
    # No member in state.
    self.assertFalse(hasattr(state_not_full, u'var3'))
    # Convert to simple.
    state_full_simple = state_not_full.ToSimple()
    # Assigned None when converted to simple.
    self.assertIn(u'var3', state_full_simple)
    self.assertIsNone(state_full_simple[u'var3'])
    
    # Delete from simple.
    del state_full_simple[u'var3']
    self.assertNotIn(u'var3', state_full_simple)
    # Recreate object.
    state_full_from_simple = StateNotFull.FromSimple(state_full_simple)
    # Assigned None when converted from simple.
    self.assertTrue(hasattr(state_full_from_simple, u'var3'))
    self.assertIsNone(state_full_from_simple.var3)
    
    # Original and recreated objects are not equal.
    self.assertNotEqual(state_not_full.HashKey(),
                        state_full_from_simple.HashKey())
    self.assertNotEqual(repr(state_not_full), repr(state_full_from_simple))
    self.assertNotEqual(state_not_full, state_full_from_simple)

  def testMultipleInheritance(self):
    derived = Derived(var1=11., var2=12., var3=13., var4=14.)
    self.AssertToFrom(derived, Base1_2)

  def testWithClassMethod(self):
    class_with_method = ClassWithMethod(3)
    with_class_method = WithClassMethod(ClassWithMethod.Method)
    self.AssertToFrom(with_class_method, WithClassMethod)
    with_class_method_from_simple = (
        WithClassMethod.FromSimple(with_class_method.ToSimple()))
    self.assertEqual(4,
                     with_class_method_from_simple.method(class_with_method, 1))
    self.assertEqual(7,
                     with_class_method_from_simple.method(class_with_method, 4))

    

if __name__ == '__main__':
    unittest.main()
