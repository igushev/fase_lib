import datetime
import hashlib

import datetime_util
import notes_database
import notes_model
import place_util
import fase
import fase_sign_in

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'


class NotesService(fase.Service):

  def OnStart(self):
    menu = self.AddMenu()
    menu.AddMenuItem(id_='user_name', text='User Name')
    menu.AddMenuItem(id_='sign_in', text='Sign In', on_click=NotesService.OnSignIn, icon='sign_in.pnp')
    sign_out_context_menu = fase.Menu()
    sign_out_context_menu.AddMenuItem(id_='sign_out_context_menu_item', text='Sign Out', on_click=NotesService.OnSignOut)
    menu.AddMenuItem(id_='sign_out', text='Sign Out', on_click_element=sign_out_context_menu, icon='sign_out.pnp')

    self.AddMainButton(text='New', on_click=NotesService.OnNew, icon='new.pnp')

    button_bar = self.AddButtonBar()
    button_bar.AddButton(id_='notes', text='Notes', on_click=NotesService.OnNotes, icon='notes.pnp')
    button_bar.AddButton(id_='favourites', text='Favourites', on_click=NotesService.OnFavourites, icon='favourites.pnp')
    button_bar.AddButton(id_='recent', text='Recent', on_click=NotesService.OnRecent, icon='recent.pnp')
    button_bar.AddButton(id_='places', text='Places', on_click=NotesService.OnPlaces, icon='places.pnp')

    self.AddStringVariable(id_='screen_label', value='notes')
    return self.OnNotes(None, None)

  def OnSignIn(self, screen, element):
    return fase_sign_in.FaseSignIn.StartSignIn(self, on_sign_in_done=NotesService.OnSignInDone, cancel_option=True)

  def OnSignInDone(self, user_id_before=None):
    assert user_id_before is not None
    self._DisplaySignInOut(logged_in=True, user_name=self.GetUser().GetUserName())

    # Move notes from guest user_id to logged in user.
    for note in notes_database.NotesDatabaseInterface.Get().GetUserNotes(user_id_before):
      note.user_id = self.GetUserId()
      notes_database.NotesDatabaseInterface.Get().AddNote(note, overwrite=True)
      
    return self._DisplayRecent(None)

  def OnSignOut(self, screen, element):
    return fase_sign_in.FaseSignIn.StartSignOut(self)

  def _DisplaySignInOut(self, logged_in=False, user_name=None):
    menu = self.GetMenu()
    if logged_in:
      assert user_name is not None
      menu.GetMenuItem(id_='user_name').SetText(user_name)
    menu.GetMenuItem(id_='user_name').SetDisplayed(logged_in)
    menu.GetMenuItem(id_='sign_in').SetDisplayed(not logged_in)
    menu.GetMenuItem(id_='sign_out').SetDisplayed(logged_in)

  def OnNotes(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('notes')
    return self._DisplayRecent(screen)

  def OnFavourites(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('favourites')
    return self._DisplayRecent(screen)

  def OnRecent(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('recent')
    return self._DisplayRecent(screen)
  
  def OnPlaces(self, screen, element):
    self.GetStringVariable(id_='screen_label').SetValue('places')
    return self._DisplayRecent(screen)

  def _DisplayRecent(self, screen):
    screen_label = self.GetStringVariable('screen_label').GetValue()
    if screen_label == 'notes':
      return self._DisplayNotesByFunc(lambda x, y: cmp(x.header, y.header), None, screen)
    elif screen_label == 'favourites':
      return self._DisplayNotesByFunc(lambda x, y: cmp(x.header, y.header), lambda x: x.favourite, screen)
    elif screen_label == 'recent':
      return self._DisplayNotesByFunc(lambda x, y: cmp(x.time, y.time), None, screen)
    elif screen_label == 'places':
      return self._DisplayNotesByFunc(lambda x, y: cmp(x.place, y.place), None, screen)
    else:
      raise AssertionError()

  # TODO(igushev): Clean up ids inside for-loop.
  def _DisplayNotesByFunc(self, cmp_func, filter_func, screen):
    screen = fase.Screen()
    notes_layout = screen.AddLayout(id_='notes_layout', orientation=fase.Layout.VERTICAL, scrollable=True)
    notes = notes_database.NotesDatabaseInterface.Get().GetUserNotes(self.GetUserId())
    if filter_func:
      notes = filter(notes, filter_func)
    for note in sorted(notes, cmp=cmp_func):
      note_layout = notes_layout.AddLayout(id_='note_layout', orientation=fase.Layout.VERTICAL, on_click=NotesService.OnNote)
      note_layout.AddStringVariable('layout_note_id', note.note_id)

      note_header_layout = note_layout.AddLayout(id_='note_header_layout', orientation=fase.Layout.HORIZONTAL)
      note_header_layout.AddLabel(id_='note_header_label', label=note.header, font=2., sizable=fase.Label.FIT_OUTER_ELEMENT)
      note_header_layout.AddImage(id_='note_header_image', image=('favourite.pnp' if note.favourite else 'favourite_non.pnp'))

      note_layout.AddLabel(id_='note_layout_label', label=note.text[:100])  # preview only

      datetime_text = datetime_util.GetDatetimeDiffStr(note.datetime, datetime.datetime.now())
      note_deails_layout = note_layout.AddLayout(id_='note_deails_layout', orientation=fase.Layout.HORIZONTAL)
      note_deails_layout.AddLabel(
          id_='note_deails_layout_datetime_text',
          label=datetime_text, font=0.75, aligh=fase.Label.LEFT, sizable=fase.Label.FIT_OUTER_ELEMENT)
      note_deails_layout.AddLabel(
          id_='note_deails_layout_place_name',
          label=note.place_name, font=0.75, aligh=fase.Label.RIGHT, sizable=fase.Label.FIT_OUTER_ELEMENT)
    return screen

  def OnNew(self, screen, element):
    return self._DisplayNote(None, screen)

  def OnNote(self, screen, element):
    note_id = element.GetStringVariable('layout_note_id')
    return self._DisplayNote(note_id, screen)

  def _DisplayNote(self, note_id, screen):
    screen = fase.Screen()
    # Don't display main controls.
    screen.SetMenuDisplayed(False)
    screen.SetMainButton(False)
    screen.SetButtonBarDisplayed(False)
    screen.EnableUtilLocation()

    note_layout = screen.AddLayout(orientation=fase.Layout.VERTICAL)
    header_text = note_layout.AddText(id_='header_text')
    text_text = note_layout.AddText(id_='text_text', sizable=fase.Label.FIT_OUTER_ELEMENT)
    favourite_bool = screen.AddBoolVariable(id_='favourite_bool', value=False)

    note = notes_database.NotesDatabaseInterface.Get().GetNote(note_id=note_id) if note_id is not None else None
    # If editing existing note.
    if note is not None:
      header_text.SetText(note.header)
      text_text.SetText(note.text)
      favourite_bool.SetValue(note.favourite)

    screen.AddStringVariable('current_note_id', note_id)
    screen.AddNextStepButton(on_click=NotesService.OnSaveNote)
    screen.AddPrevStepButton(on_click=NotesService.OnCancelNote)

    context_menu = screen.AddContextMenu('Options')
    context_menu.AddMenuItem(text=('Remove from Favourites' if favourite_bool.GetValue() else 'Add to Favourites'),
                             on_click=NotesService.OnReverseFavouriteNote,
                             icon=('favourite.pnp' if note is favourite_bool.GetValue() else 'favourite_non.pnp'))
    if note_id is not None:
      context_menu.AddMenuItem(text='Delete', icon='delete.pnp', on_click=NotesService.OnDeleteNote)

  def OnSaveNote(self, screen, element):
    note_id = screen.GetStringVariable('current_note_id')
    user_id = self.GetUserId()
    datetime_now = datetime.datetime.now()
    # If new note.
    if note_id is None:
      note_id_hash = hashlib.md5()
      note_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH))
      note_id_hash.update(user_id)
      note_id = note_id_hash.hexdigest()
    location = screen.GetUtilLocation()
    place_name = place_util.GetPlaceName(location)
    note = notes_model.Note(note_id=note_id,
                            user_id=user_id,
                            header=screen.GetElemenet(id_='header_text').GetText(),
                            text=screen.GetElement(id_='text_text').GetText(),
                            datetime=datetime_now,
                            place_name=place_name,
                            favourite=screen.GetStringVariable('favourite_bool').GetValue())
    notes_database.NotesDatabaseInterface.Get().AddNote(note, overwrite=True)
    return self._DisplayRecent(screen)

  def OnCancelNote(self, screen, element):
    return self._DisplayRecent(screen)

  def OnReverseFavouriteNote(self, screen, element):
    favourite_bool = screen.GetBoolVariable(id_='favourite_bool')
    favourite_bool.SetValue(not favourite_bool.GetValue())
    return screen

  def OnDeleteNote(self, screen, element):
    note_id = screen.GetStringVariable('current_note_id')
    if note_id is not None:
      notes_database.NotesDatabaseInterface.Get().DeleteNote(note_id)
    return self._DisplayRecent(screen)


fase.Service.RegisterService(NotesService)