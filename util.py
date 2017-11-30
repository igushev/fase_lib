def AssertIsInstance(obj, expected_type):
  if not isinstance(obj, expected_type):
    raise AssertionError('Type must be %s, but type is %s, value is %s' % (expected_type, type(obj), obj))


def AssertIsInstanceOrNone(obj, expected_type):
  if obj is not None and not isinstance(obj, expected_type):
    raise AssertionError('Type must be %s or None, but type is %s, value is %s' % (expected_type, type(obj), obj))
