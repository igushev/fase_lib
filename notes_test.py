import datetime
import unittest

import fase
import fase_database
import fase_server
import fase_model

import notes_database
import notes_model
import notes


class NotesTest(unittest.TestCase):

  def Start(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[]),
        overwrite=True)

    notes_database.NotesDatabaseInterface.Set(
        notes_database.MockNotesDatabase([
            notes_model.Note(note_id='321_1',
                             user_id='321',
                             header='Note 1 Header',
                             text='Note 1 text',
                             datetime=datetime.datetime.now(),
                             place_name='NYC',
                             favourite=False)]),
        overwrite=True)

    # Create Server and Service.
    fase_server_ = fase_server.FaseServer()
    response = fase_server_.GetService(fase_model.Device(device_type='iOS', device_token='Token'))
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')
    return fase_server_, session_info, screen_info

  def testGeneral(self):
    self.Start()

  def testNotes(self):
    fase_server_, session_info, screen_info = self.Start()

    # Click on Notes button.
    response = fase_server_.ElementClicked(
        fase_model.ElementClicked([fase.BUTTON_BAR_ID, 'notes_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')
    

if __name__ == '__main__':
    unittest.main()
