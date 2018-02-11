import copy
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

  def setUp(self):
    super(NotesTest, self).setUp()
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def Start(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[
                fase.User(user_id='321',
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

    # Create Service
    response = fase_server.FaseServer.Get().GetService(fase_model.Device(device_type='iOS', device_token='Token'))
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')
    
    return session_info, screen_info, screen

  def AssertNotes(self, expected_notes, screen):
    notes_layout = screen.GetElement(id_='notes_layout')
    for expected_note, (_, actual_note_layout) in zip(expected_notes, notes_layout.GetIdElementList()):
      if expected_note.note_id:
        self.assertEqual(expected_note.note_id, actual_note_layout.GetStringVariable(id_='layout_note_id').GetValue())
      actual_note_header_layout = actual_note_layout.GetLayout(id_='note_header_layout')
      self.assertEqual(expected_note.header, actual_note_header_layout.GetLabel(id_='note_header_label').GetLabel())
      self.assertEqual('notes_images/favourite.png' if expected_note.favourite else 'notes_images/favourite_non.png',
                       actual_note_header_layout.GetImage(id_='note_header_image').GetImage())
      self.assertEqual(expected_note.text, actual_note_layout.GetLabel(id_='note_layout_label').GetLabel())
      if expected_note.datetime:
        expected_datetime_text = datetime_util.GetDatetimeDiffStr(expected_note.datetime, datetime.datetime.now())
        actual_note_deails_layout = actual_note_layout.GetLayout(id_='note_deails_layout')
        self.assertEqual(expected_datetime_text,
                         actual_note_deails_layout.GetLabel(id_='note_deails_layout_datetime_text').GetLabel())

  def AddNote(self, session_info, screen_info, note):
    # Click on New button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.MAIN_BUTTON_ID]), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='note_layout')

    # Enter note.
    elements_update=fase_model.ElementsUpdate([['note_layout', 'header_text'],
                                               ['note_layout', 'text_text']], [note.header,
                                                                               note.text])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)

    # Click on Save button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.NEXT_STEP_BUTTON_ID]), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')

    return session_info, screen_info, screen

  def SelectNote(self, session_info, screen_info, note):
    # Click on the Note.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['notes_layout', 'note_layout_%s' % note.note_id]), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements and content.
    screen.GetElement(id_='note_layout')
    self.assertEqual(note.header, screen.GetElement(id_='note_layout').GetElement(id_='header_text').GetText())
    self.assertEqual(note.text, screen.GetElement(id_='note_layout').GetElement(id_='text_text').GetText())

    return session_info, screen_info, screen

  def EditNote(self, session_info, screen_info, note, note_edited):
    session_info, screen_info, _ = self.SelectNote(session_info, screen_info, note)

    # Edit Note.
    elements_update=fase_model.ElementsUpdate([['note_layout', 'header_text'],
                                               ['note_layout', 'text_text']], [note_edited.header,
                                                                               note_edited.text])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)

    # Click on Save button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.NEXT_STEP_BUTTON_ID]), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')

    return session_info, screen_info, screen

  def DeleteNote(self, session_info, screen_info, note):
    session_info, screen_info, _ = self.SelectNote(session_info, screen_info, note)
    
    # Click on Delete context menu.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.CONTEXT_MENU_ID, 'delete_context_menu']), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_=fase.ALERT_ID)
    # Click on Yes.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.ALERT_ID, 'ok_id']), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')

    return session_info, screen_info, screen

  def ReverseFavouriteNote(self, session_info, screen_info, note):
    session_info, screen_info, _ = self.SelectNote(session_info, screen_info, note)

    # Click on Favourite context menu.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.CONTEXT_MENU_ID, 'favourite_context_menu']), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info

    # Click on Save button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.NEXT_STEP_BUTTON_ID]), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')

    return session_info, screen_info, screen

  def testNotes_Start_SignIn_ButtonBar(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Click on Notes button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.BUTTON_BAR_ID, 'notes_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Click on Favourites button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.BUTTON_BAR_ID, 'favourites_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_2], screen)

    # Click on Recent button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.BUTTON_BAR_ID, 'recent_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_3, self.note_2], screen)

    # Click on Notes button again.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.BUTTON_BAR_ID, 'notes_button']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

  def testNotes_Start_AddNote_SignIn(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Create a Note.
    note_4 = notes_model.Note(note_id=None,
                              user_id=None,
                              header='Note 4 Header',
                              text='Note 4 text',
                              datetime=None,
                              favourite=False)

    # Add Note.
    session_info, screen_info, screen = self.AddNote(session_info, screen_info, note_4)
    self.AssertNotes([note_4], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3, note_4], screen)

  def testNotes_Start_AddNote_SignUn(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Create a Note.
    note_4 = notes_model.Note(note_id=None,
                              user_id=None,
                              header='Note 4 Header',
                              text='Note 4 text',
                              datetime=None,
                              favourite=False)

    # Add Note.
    session_info, screen_info, screen = self.AddNote(session_info, screen_info, note_4)
    self.AssertNotes([note_4], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=False,
            phone_number='+19876543210', first_name='Edward Junior', last_name='Igushev'))
    self.AssertNotes([note_4], screen)

  def testNotes_Signin_SignOut(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Sign Out.
    fase_sign_in_test_util.SignOutProcedure(session_info, screen_info,
                                            sign_out_id_list=[fase.MAIN_MENU_ID, 'sign_out_menu_item'])
    self.AssertNotes([], screen)

  def testNotes_Start_SignIn_AddNote(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Create a Note.
    note_4 = notes_model.Note(note_id=None,
                              user_id=None,
                              header='Note 4 Header',
                              text='Note 4 text',
                              datetime=None,
                              favourite=False)

    # Add Note.
    session_info, screen_info, screen = self.AddNote(session_info, screen_info, note_4)
    self.AssertNotes([self.note_1, self.note_2, self.note_3, note_4], screen)

  def testNotes_Start_SignIn_EditNote(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Copy and edit Note.
    note_2_edited = copy.copy(self.note_2)
    note_2_edited.header = 'Note 2 Header edited'
    note_2_edited.text = 'Note 2 text edited'
    note_2_edited.datetime = datetime.datetime.now()  # Should be updated by the Service.
    
    # Edit Note.
    session_info, screen_info, screen = (
        self.EditNote(session_info, screen_info, self.note_2, note_2_edited))
    self.AssertNotes([self.note_1, note_2_edited, self.note_3], screen)

  def testNotes_Start_SignIn_DeleteNote(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Delete Note.
    session_info, screen_info, screen = (
        self.DeleteNote(session_info, screen_info, self.note_2))
    self.AssertNotes([self.note_1, self.note_3], screen)

  def testNotes_Start_SignIn_ReverseFavouriteNote(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Copy and edit Note.
    note_3_edited = copy.copy(self.note_3)
    note_3_edited.favourite = True
    note_3_edited.datetime = datetime.datetime.now()  # Should be updated by the Service.
    
    # Reverse Favourite for Note.
    session_info, screen_info, screen = (
        self.ReverseFavouriteNote(session_info, screen_info, self.note_3))
    self.AssertNotes([self.note_1, self.note_2, note_3_edited], screen)

  def testNotes_Start_SignIn_EditNote_Cancel(self):
    session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            session_info, screen_info,
            sign_in_id_list=[fase.MAIN_MENU_ID, 'sign_in_menu_item'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Copy and edit Note.
    note_2_edited = copy.copy(self.note_2)
    note_2_edited.header = 'Note 2 Header edited'
    note_2_edited.text = 'Note 2 text edited'

    session_info, screen_info, screen = self.SelectNote(session_info, screen_info, self.note_2)

    # Edit Note.
    elements_update=fase_model.ElementsUpdate([['note_layout', 'header_text'],
                                               ['note_layout', 'text_text']], [note_2_edited.header,
                                                                               note_2_edited.text])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)

    # Click on Cancel button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=[fase.PREV_STEP_BUTTON_ID]), session_info, screen_info)
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_layout')
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)



if __name__ == '__main__':
    unittest.main()
