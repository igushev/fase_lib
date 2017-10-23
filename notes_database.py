import singleton_util


@singleton_util.Singleton()
class NotesDatabaseInterface(object):

  def GetUserNotes(self, user_id):
    raise NotImplemented()


class MockNotesDatabase(NotesDatabaseInterface):

  def __init__(self, notes):
    self.notes = notes

  def GetUserNotes(self, user_id):
    return [note for note in self.notes if note.user_id == user_id]
