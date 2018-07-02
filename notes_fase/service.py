import datetime
import hashlib

from base_util import datetime_util
from server_util import version_util

from fase import fase
from fase import fase_sign_in

from notes_fase import database as notes_database
from notes_fase import model as notes_model


CREATE_DB_COMMAND = 'createdb'
DELETE_DB_COMMAND = 'deletedb'

TABLES_CREATED = 'Add table are being created'
TABLES_DELETED = 'All tables are being deleted'

WRONG_COMMAND = 'Wrong command!'
DELETING_DB_IS_NOT_ALLOWED = 'Deleting of database is not allowed by the configuration!'

NOTES_VERSION_FILENAME = 'notes_fase/version.txt'

SELECTED_ICON = 'solid_blue'
NAVIGATION_ICON = 'color'
PREVIEW_LENGTH = 50


class NotesService(fase.Service):

  allow_deletedb = False

  @staticmethod
  def GetServiceId():
    return 'Notes'

  @staticmethod
  def ServiceCommand(command):
    if command.command == CREATE_DB_COMMAND:
      notes_database.NotesDatabaseInterface.Get().CreateDatabase()
      return TABLES_CREATED
    elif command.command == DELETE_DB_COMMAND:
      if not NotesService.allow_deletedb:
        raise AssertionError(DELETING_DB_IS_NOT_ALLOWED)
      notes_database.NotesDatabaseInterface.Get().DeleteDatabase()
      return TABLES_DELETED
    else:
      raise AssertionError(WRONG_COMMAND)

  version = version_util.ReadVersion(NOTES_VERSION_FILENAME)

  @staticmethod
  def Version():
    return NotesService.version

  def OnStart(self):
    self.AddStringVariable(id_='screen_label', value='notes')
    return self.OnNotes(None, None)

  def OnNotes(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('notes')
    return self._DisplayNotes(screen)

  def OnFavourites(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('favourites')
    return self._DisplayNotes(screen)

  def OnRecent(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('recent')
    return self._DisplayNotes(screen)
  
  def _DisplayNotes(self, screen):
    screen_label = self.GetStringVariable(id_='screen_label').GetValue()
    if screen_label == 'notes':
      return self._DisplayNotesByFunc(screen_label, lambda note: note.header, False, None, 'Notes', screen)
    elif screen_label == 'favourites':
      return self._DisplayNotesByFunc(screen_label, lambda note: note.header, False, lambda x: x.favourite, 'Favourites', screen)
    elif screen_label == 'recent':
      return self._DisplayNotesByFunc(screen_label, lambda note: note.datetime, True, None, 'Recent', screen)
    else:
      raise AssertionError(screen_label)

  def _DisplayNotesByFunc(self, screen_label, key_func, reverse, filter_func, title, screen):
    screen = fase.Screen(self)
    screen.SetTitle(title)
    screen.SetScrollable(True)
    self._AddButtons(screen, screen_label)
    notes_frame = screen.AddFrame(id_='notes_frame', orientation=fase.Frame.VERTICAL)
    notes = notes_database.NotesDatabaseInterface.Get().GetUserNotes(self.GetUserId())
    if filter_func:
      notes = filter(filter_func, notes)
    for note in sorted(notes, key=key_func, reverse=reverse):
      note_frame = notes_frame.AddFrame(
          id_='note_frame_%s' % note.note_id, orientation=fase.Frame.VERTICAL, border=True,
          on_click=NotesService.OnNote)
      note_frame.AddStringVariable(id_='frame_note_id', value=note.note_id)

      note_header_frame = note_frame.AddFrame(
          id_='note_header_frame', orientation=fase.Frame.HORIZONTAL, size=fase.Label.MAX)
      note_header_frame.AddLabel(
          id_='note_header_label', text=note.header, font=fase.Font(size=1.5),
          size=fase.Label.MAX, align=fase.Label.LEFT)
      note_header_frame.AddImage(
          id_='note_header_image', filename=('images/favourite_2/favourite_orange_@.png' if note.favourite else
                                             'images/favourite_2/favourite_frame_black_@.png'), pixel_density_mult=2.0)

      note_frame.AddLabel(id_='note_frame_label', text=note.text[:PREVIEW_LENGTH], align=fase.Label.LEFT)

      datetime_text = datetime_util.GetDatetimeDiffStr(note.datetime, datetime.datetime.utcnow())
      note_deails_frame = note_frame.AddFrame(id_='note_deails_frame', orientation=fase.Frame.HORIZONTAL)
      note_deails_frame.AddLabel(
          id_='note_deails_frame_datetime_text', text=datetime_text, font=fase.Font(size=0.75),
          size=fase.Label.MAX, align=fase.Label.RIGHT)
    return screen

  def _AddButtons(self, screen, screen_label):
    screen.AddMainButton(text='New', image=fase.Image(filename='images/new/new_%s_@.png' % NAVIGATION_ICON),
                         on_click=NotesService.OnNew)
    navigation = screen.AddNavigation()
    navigation.AddButton(id_='notes_button', text='Notes',
                         image=fase.Image(filename='images/notes/notes_%s_@.png' %
                                          (SELECTED_ICON if screen_label == 'notes' else NAVIGATION_ICON)),
                         on_click=NotesService.OnNotes)
    navigation.AddButton(id_='favourites_button', text='Favourites',
                         image=fase.Image(filename='images/favourites/favourites_%s_@.png' %
                                          (SELECTED_ICON if screen_label == 'favourites' else NAVIGATION_ICON)),
                         on_click=NotesService.OnFavourites)
    navigation.AddButton(id_='recent_button', text='Recent',
                         image=fase.Image(filename='images/recent/recent_%s_@.png' %
                                          (SELECTED_ICON if screen_label == 'recent' else NAVIGATION_ICON)),
                         on_click=NotesService.OnRecent)
    if self.IfSignedIn():
      navigation.AddButton(id_='sign_out_button', text='Sign Out',
                           image=fase.Image(filename='images/account/account_%s_@.png' % NAVIGATION_ICON),
                           on_click=NotesService.OnSignOut)
    else:
      navigation.AddButton(id_='sign_in_button', text='Sign In',
                           image=fase.Image(filename='images/account/account_%s_@.png' % NAVIGATION_ICON),
                           on_click=NotesService.OnSignIn)

  def OnSignIn(self, screen, element):
    return fase_sign_in.StartSignIn(self, on_done=NotesService.OnSignInDone, on_cancel=NotesService.OnSignInOutCancel)

  def OnSignInDone(self, user_id_before=None):
    assert user_id_before is not None
    # Move notes from guest user_id to logged in user.
    for note in notes_database.NotesDatabaseInterface.Get().GetUserNotes(user_id_before):
      note.user_id = self.GetUserId()
      notes_database.NotesDatabaseInterface.Get().AddNote(note, overwrite=True)
      
    return self._DisplayNotes(None)

  def OnSignOut(self, screen, element):
    return fase_sign_in.StartSignOut(self, on_cancel=NotesService.OnSignInOutCancel)

  def OnSignInOutCancel(self):
    return self._DisplayNotes(None)

  def OnNew(self, screen, element):
    return self._DisplayNote(None, screen)

  def OnNote(self, screen, element):
    note_id = element.GetStringVariable(id_='frame_note_id').GetValue()
    return self._DisplayNote(note_id, screen)

  def _DisplayNote(self, note_id, screen):
    screen = fase.Screen(self)
    screen.AddStringVariable(id_='current_note_id', value=note_id)
    note = notes_database.NotesDatabaseInterface.Get().GetNote(note_id=note_id) if note_id is not None else None
    favourite_bool = screen.AddBoolVariable(id_='favourite_bool', value=note is not None and note.favourite)

    note_frame = screen.AddFrame(id_='note_frame', orientation=fase.Frame.VERTICAL, size=fase.Frame.MAX)
    note_frame.AddImage(id_='favourite_image',
                        filename=('images/favourite_2/favourite_orange_@.png' if favourite_bool.GetValue() else
                                  'images/favourite_2/favourite_frame_black_@.png'), pixel_density_mult=2.0,
                        align=fase.Image.RIGHT, on_click=NotesService.OnReverseFavouriteNote)
    header_text = note_frame.AddText(id_='header_text', hint='Header')
    text_text = note_frame.AddText(id_='text_text', hint='Text', size=fase.Label.MAX, multiline=True)
    if note_id is not None:
      note_frame.AddImage(id_='delete_image', filename='images/delete/delete_color_@.png', pixel_density_mult=2.0,
                          align=fase.Image.RIGHT, on_click=NotesService.OnDeleteNote)

    # If editing existing note.
    if note is not None:
      header_text.SetText(note.header)
      text_text.SetText(note.text)

    screen.AddNextStepButton(text='Save', on_click=NotesService.OnSaveNote)
    screen.AddPrevStepButton(text='Back', on_click=NotesService.OnCancelNote)
    return screen

  def OnSaveNote(self, screen, element):
    note_id = screen.GetStringVariable(id_='current_note_id').GetValue()
    user_id = self.GetUserId()
    datetime_now = datetime.datetime.utcnow()
    # If new note.
    if note_id is None:
      note_id_hash = hashlib.md5()
      note_id_hash.update(datetime_now.strftime(fase.DATETIME_FORMAT_HASH).encode('utf-8'))
      note_id_hash.update(user_id.encode('utf-8'))
      note_id = note_id_hash.hexdigest()
    note_frame = screen.GetFrame(id_='note_frame')
    note = notes_model.Note(note_id=note_id,
                            user_id=user_id,
                            header=note_frame.GetElement(id_='header_text').GetText(),
                            text=note_frame.GetElement(id_='text_text').GetText(),
                            datetime=datetime_now,
                            favourite=screen.GetStringVariable(id_='favourite_bool').GetValue())
    notes_database.NotesDatabaseInterface.Get().AddNote(note, overwrite=True)
    return self._DisplayNotes(screen)

  def OnCancelNote(self, screen, element):
    return self._DisplayNotes(screen)

  def OnReverseFavouriteNote(self, screen, element):
    favourite_bool = screen.GetBoolVariable(id_='favourite_bool')
    favourite_bool.SetValue(not favourite_bool.GetValue())
    screen.GetFrame(id_='note_frame').GetImage(id_='favourite_image').SetFilename(
        'images/favourite_2/favourite_orange_@.png' if favourite_bool.GetValue() else
        'images/favourite_2/favourite_frame_black_@.png')
    return screen

  def OnDeleteNote(self, screen, element):
    note_id = screen.GetStringVariable(id_='current_note_id').GetValue()
    screen = fase.Screen(self)
    alert = screen.AddAlert('Delete the Note?')
    alert.AddButton(id_="ok_id", text="OK", on_click=NotesService.OnDeleteNoteOK)
    alert.AddButton(id_="cancel_id", text="Cancel", on_click=NotesService.OnDeleteNoteCancel)
    screen.AddStringVariable(id_='current_note_id', value=note_id)
    return screen

  def OnDeleteNoteOK(self, screen, element):
    note_id = screen.GetStringVariable(id_='current_note_id').GetValue()
    if note_id is not None:
      notes_database.NotesDatabaseInterface.Get().DeleteNote(note_id)
    return self._DisplayNotes(screen)

  def OnDeleteNoteCancel(self, screen, element):
    note_id = screen.GetStringVariable(id_='current_note_id').GetValue()
    return self._DisplayNote(note_id, screen)

fase.Service.RegisterService(NotesService)