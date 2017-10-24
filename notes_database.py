import singleton_util


@singleton_util.Singleton()
class NotesDatabaseInterface(object):

  def GetUserNotes(self, user_id):
    raise NotImplemented()


class MockNotesDatabase(NotesDatabaseInterface):

  def __init__(self, note_list):
    self.note_list = note_list

  def GetUserNotes(self, user_id):
    return [note for note in self.note_list if note.user_id == user_id]
