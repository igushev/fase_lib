import singleton_util


@singleton_util.Singleton()
class NotesDatabaseInterface(object):

  def GetUserNotes(self, user_id):
    raise NotImplemented()


class MockNotesDatabase(NotesDatabaseInterface):

  def __init__(self, note_list):
    self.note_id_note = {note.note_id: note for note in note_list}

  def GetUserNotes(self, user_id):
    return [note for note in self.note_id_note.itervalues() if note.user_id == user_id]

  def AddNote(self, note, overwrite=False):
    assert note.note_id not in self.note_id_note or overwrite
    self.note_id_note[note.note_id] = note
