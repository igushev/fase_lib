import copy
import datetime
import unittest

from base_util import datetime_util
from server_util import resource_manager

from fase import fase
from fase_model import fase_model
from fase_server import fase_database
from fase_server import fase_resource
from fase_server import fase_server
from fase_server import fase_sign_in_test_util

from notes_fase import database as notes_database
from notes_fase import model as notes_model
from notes_fase import service as notes_service


class NotesTest(unittest.TestCase):

  def setUp(self):
    super(NotesTest, self).setUp()
    resource_manager.ResourceManager.Set(
        resource_manager.ResourceManager(fase_resource.GetResourceDir()), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def Start(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_prog_list=[],
            screen_prog_list=[],
            user_list=[
                fase.User(user_id='321',
                          phone_number='+13216549870',
                          first_name='Edward',
                          last_name='Igushev',
                          datetime_added=datetime.datetime.utcnow())]),
        overwrite=True)

    datetime_now = datetime.datetime.utcnow()
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
    self.device = fase_model.Device(device_type='Python', device_id='DeviceID')
    response = fase_server.FaseServer.Get().GetService(self.device)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_frame')
    
    return version_info, session_info, screen_info, screen

  def AssertNotes(self, expected_notes, screen):
    notes_frame = screen.GetElement(id_='notes_frame')
    for expected_note, (actual_note_frame_id, actual_note_frame) in zip(expected_notes, notes_frame.GetIdElementList()):
      if expected_note.note_id:
        self.assertEqual('note_frame_%s' % expected_note.note_id, actual_note_frame_id)
        # Actual variable removed from output.
        self.assertFalse(actual_note_frame.HasStringVariable(id_='frame_note_id'))
      actual_note_header_frame = actual_note_frame.GetFrame(id_='note_header_frame')
      self.assertEqual(expected_note.header, actual_note_header_frame.GetLabel(id_='note_header_label').GetText())
      self.assertEqual('images/favourite_2/favourite_orange_1_00.png' if expected_note.favourite else
                       'images/favourite_2/favourite_frame_black_1_00.png',
                       actual_note_header_frame.GetImage(id_='note_header_image').GetFilename())
      self.assertEqual(expected_note.text, actual_note_frame.GetLabel(id_='note_frame_label').GetText())
      if expected_note.datetime:
        expected_datetime_text = datetime_util.GetDatetimeDiffStr(expected_note.datetime, datetime.datetime.utcnow())
        actual_note_deails_frame = actual_note_frame.GetFrame(id_='note_deails_frame')
        self.assertEqual(expected_datetime_text,
                         actual_note_deails_frame.GetLabel(id_='note_deails_frame_datetime_text').GetText())

  def AddNote(self, version_info, session_info, screen_info, note):
    # Click on New button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.MAIN_BUTTON_ID], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.screen_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='note_frame')

    # Enter note.
    elements_update=fase_model.ElementsUpdate([['note_frame', 'header_text'],
                                               ['note_frame', 'text_text']], [note.header,
                                                                              note.text])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=self.device)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, version_info, session_info, screen_info)

    # Click on Save button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NEXT_STEP_BUTTON_ID], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.screen_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_frame')

    return version_info, session_info, screen_info, screen

  def SelectNote(self, version_info, session_info, screen_info, note):
    # Click on the Note.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(
            id_list=['notes_frame', 'note_frame_%s' % note.note_id], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements and content.
    screen.GetElement(id_='note_frame')
    self.assertEqual(note.header, screen.GetElement(id_='note_frame').GetElement(id_='header_text').GetText())
    self.assertEqual(note.text, screen.GetElement(id_='note_frame').GetElement(id_='text_text').GetText())

    return version_info, session_info, screen_info, screen

  def EditNote(self, version_info, session_info, screen_info, note, note_edited):
    version_info, session_info, screen_info, _ = self.SelectNote(version_info, session_info, screen_info, note)

    # Edit Note.
    elements_update=fase_model.ElementsUpdate([['note_frame', 'header_text'],
                                               ['note_frame', 'text_text']], [note_edited.header,
                                                                               note_edited.text])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=self.device)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, version_info, session_info, screen_info)

    # Click on Save button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NEXT_STEP_BUTTON_ID], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_frame')

    return version_info, session_info, screen_info, screen

  def DeleteNote(self, version_info, session_info, screen_info, note):
    version_info, session_info, screen_info, _ = self.SelectNote(version_info, session_info, screen_info, note)
    
    # Click on Delete image.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=['note_frame', 'delete_image'], method=fase.ON_CLICK_METHOD,
                                   device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_=fase.ALERT_ID)
    # Click on Yes.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.ALERT_ID, 'ok_id'], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_frame')

    return version_info, session_info, screen_info, screen

  def ReverseFavouriteNote(self, version_info, session_info, screen_info, note):
    version_info, session_info, screen_info, _ = self.SelectNote(version_info, session_info, screen_info, note)

    # Click on Favourite image.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=['note_frame', 'favourite_image'], method=fase.ON_CLICK_METHOD,
                                   device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info

    # Click on Save button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NEXT_STEP_BUTTON_ID], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_frame')

    return version_info, session_info, screen_info, screen

  def testNotes_Start_SignIn_Navigation(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Click on Notes button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NAVIGATION_ID, 'notes_button'], method=fase.ON_CLICK_METHOD,
                                   device=self.device),
        version_info, session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Click on Favourites button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NAVIGATION_ID, 'favourites_button'], method=fase.ON_CLICK_METHOD,
                                   device=self.device),
        version_info, session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_2], screen)

    # Click on Recent button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NAVIGATION_ID, 'recent_button'], method=fase.ON_CLICK_METHOD,
                                   device=self.device),
        version_info, session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_3, self.note_2], screen)

    # Click on Notes button again.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.NAVIGATION_ID, 'notes_button'], method=fase.ON_CLICK_METHOD,
                                   device=self.device),
        version_info, session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

  def testNotes_Start_AddNote_SignIn(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Create a Note.
    note_4 = notes_model.Note(note_id=None,
                              user_id=None,
                              header='Note 4 Header',
                              text='Note 4 text',
                              datetime=None,
                              favourite=False)

    # Add Note.
    version_info, session_info, screen_info, screen = self.AddNote(version_info, session_info, screen_info, note_4)
    self.AssertNotes([note_4], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3, note_4], screen)

  def testNotes_Start_AddNote_SignUn(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Create a Note.
    note_4 = notes_model.Note(note_id=None,
                              user_id=None,
                              header='Note 4 Header',
                              text='Note 4 text',
                              datetime=None,
                              favourite=False)

    # Add Note.
    version_info, session_info, screen_info, screen = self.AddNote(version_info, session_info, screen_info, note_4)
    self.AssertNotes([note_4], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=False,
            phone_number='+19876543210', first_name='Edward Junior', last_name='Igushev'))
    self.AssertNotes([note_4], screen)

  def testNotes_Signin_SignOut(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Sign Out.
    fase_sign_in_test_util.SignOutProcedure(version_info, session_info, screen_info,
                                            sign_out_id_list=[fase.NAVIGATION_ID, 'sign_out_button'])
    self.AssertNotes([], screen)

  def testNotes_Start_SignIn_AddNote(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Create a Note.
    note_4 = notes_model.Note(note_id=None,
                              user_id=None,
                              header='Note 4 Header',
                              text='Note 4 text',
                              datetime=None,
                              favourite=False)

    # Add Note.
    version_info, session_info, screen_info, screen = self.AddNote(version_info, session_info, screen_info, note_4)
    self.AssertNotes([self.note_1, self.note_2, self.note_3, note_4], screen)

  def testNotes_Start_SignIn_EditNote(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Copy and edit Note.
    note_2_edited = copy.copy(self.note_2)
    note_2_edited.header = 'Note 2 Header edited'
    note_2_edited.text = 'Note 2 text edited'
    note_2_edited.datetime = datetime.datetime.utcnow()  # Should be updated by the Service.
    
    # Edit Note.
    version_info, session_info, screen_info, screen = (
        self.EditNote(version_info, session_info, screen_info, self.note_2, note_2_edited))
    self.AssertNotes([self.note_1, note_2_edited, self.note_3], screen)

  def testNotes_Start_SignIn_DeleteNote(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Delete Note.
    version_info, session_info, screen_info, screen = (
        self.DeleteNote(version_info, session_info, screen_info, self.note_2))
    self.AssertNotes([self.note_1, self.note_3], screen)

  def testNotes_Start_SignIn_ReverseFavouriteNote(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Copy and edit Note.
    note_3_edited = copy.copy(self.note_3)
    note_3_edited.favourite = True
    note_3_edited.datetime = datetime.datetime.utcnow()  # Should be updated by the Service.
    
    # Reverse Favourite for Note.
    version_info, session_info, screen_info, screen = (
        self.ReverseFavouriteNote(version_info, session_info, screen_info, self.note_3))
    self.AssertNotes([self.note_1, self.note_2, note_3_edited], screen)

  def testNotes_Start_SignIn_EditNote_Cancel(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Sign In.
    version_info, session_info, screen_info, screen = (
        fase_sign_in_test_util.SignInProcedure(
            version_info, session_info, screen_info,
            sign_in_id_list=[fase.NAVIGATION_ID, 'sign_in_button'], sign_in=True, phone_number='+13216549870'))
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

    # Copy and edit Note.
    note_2_edited = copy.copy(self.note_2)
    note_2_edited.header = 'Note 2 Header edited'
    note_2_edited.text = 'Note 2 text edited'

    version_info, session_info, screen_info, screen = self.SelectNote(
        version_info, session_info, screen_info, self.note_2)

    # Edit Note.
    elements_update=fase_model.ElementsUpdate([['note_frame', 'header_text'],
                                               ['note_frame', 'text_text']], [note_2_edited.header,
                                                                              note_2_edited.text])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=self.device)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, version_info, session_info, screen_info)

    # Click on Cancel button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=[fase.PREV_STEP_BUTTON_ID], method=fase.ON_CLICK_METHOD, device=self.device),
        version_info, session_info, screen_info)
    version_info = response.version_info 
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='notes_frame')
    self.AssertNotes([self.note_1, self.note_2, self.note_3], screen)

  def testNotes_EmptyHeader(self):
    version_info, session_info, screen_info, screen = self.Start()
    self.AssertNotes([], screen)

    # Create a Note.
    note = notes_model.Note(note_id=None,
                            user_id=None,
                            header='',
                            text='',
                            datetime=None,
                            favourite=False)

    # Add Note.
    version_info, session_info, screen_info, screen = self.AddNote(version_info, session_info, screen_info, note)
    self.AssertNotes([note], screen)


if __name__ == '__main__':
    unittest.main()
