import unittest
import datetime

import datetime_util


class DateUtilsTest(unittest.TestCase):
  
  def testGetDatetimeDiffStr(self):
    datetime_from = datetime.datetime(2017, 5, 22, 12, 0, 0)
    
    def TestGetDatetimeDiffStr(datetime_diff_str, timedelta):
      self.assertEqual(
          datetime_diff_str,
          datetime_util.GetDatetimeDiffStr(
              datetime_from, datetime_from+timedelta))
    
    TestGetDatetimeDiffStr('Just now',
                           datetime.timedelta(seconds=15))
    TestGetDatetimeDiffStr('Just now',
                           datetime.timedelta(seconds=45))
    TestGetDatetimeDiffStr('15 minutes ago',
                           datetime.timedelta(minutes=15, seconds=15))
    TestGetDatetimeDiffStr('45 minutes ago',
                           datetime.timedelta(minutes=45, seconds=15))
    TestGetDatetimeDiffStr('3 hours ago',
                           datetime.timedelta(hours=3, seconds=15))
    TestGetDatetimeDiffStr('12 hours ago',
                           datetime.timedelta(hours=12, seconds=15))
    TestGetDatetimeDiffStr('Yesterday',
                           datetime.timedelta(days=1, seconds=15))
    TestGetDatetimeDiffStr('May/22/17',
                           datetime.timedelta(days=2, seconds=15))
    TestGetDatetimeDiffStr('May/22/17',
                           datetime.timedelta(days=3, seconds=15))
    
    

if __name__ == '__main__':
    unittest.main()
