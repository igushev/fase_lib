class AbstractObject(object):

  def __str__(self):
    return '\n'.join(['%s: %s' % (key.replace('_', ' ').title(), value)
                      for key, value in self.__dict__.iteritems()])

  def __eq__(self, other):
    return self.__dict__ == other.__dict__
