import data_util
import json_util


@json_util.JSONDecorator(
    {'note_id': json_util.JSONString(),
     'user_id': json_util.JSONString(),
     'header': json_util.JSONString(),
     'text': json_util.JSONString(),
     'datetime': json_util.JSONDateTime(),
     'favourite': json_util.JSONBool()})
class Note((data_util.AbstractObject)):
  
  def __init__(self,
               note_id=None,
               user_id=None,
               header=None,
               text=None,
               datetime=None,
               favourite=None):
    self.note_id = note_id
    self.user_id = user_id
    self.header = header
    self.text = text
    self.datetime = datetime
    self.favourite = favourite
