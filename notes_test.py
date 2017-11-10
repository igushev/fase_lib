import datetime
import unittest

import fase
import fase_database
import fase_server
import fase_model
import fase_sign_in_test_util

import datetime_util
import notes_database
import notes_model
import notes


class NotesTest(unittest.TestCase):

  def Start(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[
                fase_model.User(user_id='321',
                                phone_number='+13216549870',
                                first_name='Edward',
                                last_name='Igushev',
                                datetime_added=datetime.datetime.now())]),
        overwrite=True)

    datetime_now = datetime.datetime.now()
    self.note_1 = notes_model.Note(note_id='321_1',
                                   user_id='321',
                                   header='Note 1 Header',
                                   text='Note 1 text',
                                   datetime=datetime_now+datetime.timedelta(days=1),
                                   favourite=False)
    self.note_2 = notes_model.Note(note_id='321_2',
                                   user_id='321',
                                   header='Note 2 Header',
                                   text='Note 2 text',
                                   datetime=datetime_now-datetime.timedelta(days=1),
                                   favourite=True)
    self.note_3 = notes_model.Note(note_id='321_3',
                                   user_id='321',
                                   header='Note 3 Header',
                                   text='Note 3 text',
                                   datetime=datetime_now,
                                   favourite=False)  
    notes_database.NotesDatabaseInterface.Set(
        notes_database.MockNotesDatabase([self.note_1, self.note_2, self.note_3]),
        overwrite=True)

    # Create Server and Service.
    fase_server_ = fase_server.FaseServer()
    response = fase_server_.GetService(fase_model.Device(device_type='iOS', device_token='Token'))
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')
    
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            fase_server_, session_info, screen_info,
            sign_in_id_list=[fase.MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')
    
    return fase_server_, session_info, screen_info, screen

  def AssertNotes(self, expected_notes, screen):
    notes_layout = screen.GetElement(id_='notes_layout')
    for expected_note, (_, actual_note_layout) in zip(expected_notes, notes_layout.GetIdElementList()):
      self.assertEqual(expected_note.note_id, actual_note_layout.GetStringVariable(id_='layout_note_id').GetValue())
      actual_note_header_layout = actual_note_layout.GetLayout(id_='note_header_layout')
      self.assertEqual(expected_note.header, actual_note_header_layout.GetLabel(id_='note_header_label').GetLabel())
      self.assertEqual('favourite.pnp' if expected_note.favourite else 'favourite_non.pnp',
                       actual_note_header_layout.GetImage(id_='note_header_image').GetImage())
      self.assertEqual(expected_note.text, actual_note_layout.GetLabel(id_='note_layout_label').GetLabel())
      expected_datetime_text = datetime_util.GetDatetimeDiffStr(expected_note.datetime, datetime.datetime.now())
      actual_note_deails_layout = actual_note_layout.GetLayout(id_='note_deails_layout')
      
      self.assertEqual(expected_datetime_text,
                       actual_note_deails_layout.GetLabel(id_='note_deails_layout_datetime_text').GetLabel())

  def testNotes(self):
    fase_server_, session_info, screen_info, screen = self.Start()
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Click on Notes button.
    response = fase_server_.ElementClicked(
        fase_model.ElementClicked([fase.BUTTON_BAR_ID, 'notes_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Click on Favourites button.
    response = fase_server_.ElementClicked(
        fase_model.ElementClicked([fase.BUTTON_BAR_ID, 'favourites_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_2], screen)

    # Click on Recent button.
    response = fase_server_.ElementClicked(
        fase_model.ElementClicked([fase.BUTTON_BAR_ID, 'recent_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_2, self.note_3, self.note_1], screen)

    # Click on Notes button again.
    response = fase_server_.ElementClicked(
        fase_model.ElementClicked([fase.BUTTON_BAR_ID, 'notes_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)
    

if __name__ == '__main__':
    unittest.main()
