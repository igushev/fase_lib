import unittest

import singleton_util


@singleton_util.Singleton()
class SumClass(object):
  
  def __init__(self, a, b):
    self._a = a
    self._b = b
    
  def Sum(self):
    return self._a + self._b


class SingletonTest(unittest.TestCase):

  def testSingleton(self):
    self.assertRaises(AssertionError, SumClass.Get)
    self.assertRaises(AssertionError, SumClass.Set, int)
    SumClass.Set(SumClass(2, 1))
    self.assertEqual(3, SumClass.Get().Sum())
    self.assertRaises(AssertionError, SumClass.Set, SumClass(1, 2))
    

if __name__ == '__main__':
    unittest.main()
