class Note(object):
  
  def __init__(self,
               note_id=None,
               user_id=None,
               header=None,
               text=None,
               datetime=None,
               place_name=None,
               favourite=None):
    self.note_id = note_id
    self.user_id = user_id
    self.header = header
    self.text = text
    self.datetime = datetime
    self.place_name = place_name
    self.favourite = favourite
