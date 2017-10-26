import datetime
import unittest

import notes_database
import notes_model
import notes


class NotesTest(unittest.TestCase):

  def testGeneral(self):
    notes_database.NotesDatabaseInterface.Set(notes_database.MockNotesDatabase([
        notes_model.Note(note_id='321_1',
                         user_id='321',
                         header='Note 1 Header',
                         text='Note 1 text',
                         datetime=datetime.datetime.now(),
                         place_name='NYC',
                         favourite=False)]))
    notes_service = notes.NotesService()
    notes_service.SetUserId('321')
    screen = notes_service.OnStart()
    
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(screen.ToSimple())
    
    

if __name__ == '__main__':
    unittest.main()
