import datetime


DATETIME_FORMAT_DATE = '%B/%d/%y'


def GetDatetimeDiffStr(datetime_from, datetime_to):
    datetime_diff = datetime_to - datetime_from
    datetime_diff_total_seconds = datetime_diff.total_seconds()
    if datetime_diff_total_seconds < 60:  # Less than minute ago
      return 'Just now'
    elif datetime_diff_total_seconds < 60*60:  # Less than hour ago
      return '%d minutes ago' % (datetime_diff_total_seconds // 60)
    elif datetime_diff_total_seconds < 60*60*24:  # Less than day ago
      return '%d hours ago' %  (datetime_diff_total_seconds // (60*60))
    elif datetime_diff_total_seconds < 60*60*24*2:  # Less than two days ago
      return 'Yesterday'
    return datetime_from.strftime(DATETIME_FORMAT_DATE)
