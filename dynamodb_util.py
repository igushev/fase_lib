def SimpleToField(simple):
  if isinstance(simple, list):
    return {'L': [SimpleToField(nested_simple) for nested_simple in simple]}
  elif isinstance(simple, dict):
    return {'M': {nested_key: SimpleToField(nested_simple) for nested_key, nested_simple in simple.iteritems()}}
  elif isinstance(simple, basestring):
    return {'S': simple}
  elif isinstance(simple, bool):
    return {'BOOL': simple}
  elif isinstance(simple, (float, int)):
    return {'N': str(simple)}
  elif simple is None:
    return {'NULL': True}
  else:
    raise TypeError('Unsupported type: %s' % type(simple))


def SimpleToItem(simple):
  return {nested_key: SimpleToField(nested_simple) for nested_key, nested_simple in simple.iteritems()}


def FieldToSimple(type_item):
  assert isinstance(type_item, dict)
  assert len(type_item) == 1
  type_, item = list(type_item.iteritems())[0]
  if type_ == 'L':
    return [FieldToSimple(nested_type_item) for nested_type_item in item]
  elif type_ == 'M':
    return {nested_key: FieldToSimple(nested_type_item)
            for nested_key, nested_type_item in item.iteritems()}
  elif type_ == 'S':
    return str(item)
  elif type_ == 'BOOL':
    return item
  elif type_ == 'N':
    return float(item)
  elif type_ == 'NULL':
    assert item is True
    return None
  else:
    return TypeError('Unsorted type: %s' % type_)


def ItemToSimple(item):
  return {nested_key: FieldToSimple(nested_type_item) for nested_key, nested_type_item in item.iteritems()} 
