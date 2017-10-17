import datetime
import functools
import hashlib

import datetime_util
import notes_database
import notes_model
import place_util
import fase
import fase_sign_in_util

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'


class NotesService(fase.Service, fase_sign_in_util.SignInUtil):

  def OnStart(self):
    menu = self.AddMenu()
    menu.AddMenuItem(id_='user_name', text='User Name')
    menu.AddMenuItem(id_='sign_in', text='Sign In', on_click=self.OnSignIn, icon='sign_in.pnp')
    sign_out_context_menu = fase.ContextMenu('Sign Out')
    sign_out_context_menu.AddMenuItem(id_='sign_out_context_menu_item', text='Sign Out', on_click=self.OnSignOut)
    menu.AddMenuItem(id_='sign_out', text='Sign Out', on_click=sign_out_context_menu, icon='sign_out.pnp')

    self.AddMainButton(text='New', on_click=self.OnNew, icon='new.pnp')

    button_bar = self.AddButtonBar()
    button_bar.AddButton(id_='notes', text='Notes', on_click=self.OnNotes, icon='notes.pnp')
    button_bar.AddButton(id_='favourites', text='Favourites', on_click=self.OnFavourites, icon='favourites.pnp')
    button_bar.AddButton(id_='recent', text='Recent', on_click=self.OnRecent, icon='recent.pnp')
    button_bar.AddButton(id_='places', text='Places', on_click=self.OnPlaces, icon='places.pnp')

    self.AddStringVariable(id_='screen_label')
    return self.OnNotes(None)

  def OnSignIn(self, screen):
    screen.AddStringVariable('previous_user_id', self.GetUserId())
    return self.SignInProcedure(screen, skip_option=False, cancel_option=True, on_done=self.OnSignInDone)

  def OnSignInDone(self, screen, sign_in_cancelled):
    if not sign_in_cancelled:
      previous_user_id = screen.GetStringVariable('previous_user_id').GetValue()
      self._DisplaySignInOut(logged_in=True, user_name=self.GetUser().GetUserName())
  
      # Move notes from guest user_id to logged in user.
      for note in notes_database.NotesDatabase.Get().GetUserNotes(previous_user_id):
        note.user_id = self.GetUserId()
        notes_database.NotesDatabase.Get().AddNote(note, overwrite=True)
      
    return self._DisplayRecent(screen)

  def OnSignOut(self, screen):
    self.ResetUserId()
    return self._DisplayRecent(screen)

  def _DisplaySignInOut(self, logged_in=False, user_name=None):
    menu = self.GetMenu()
    if logged_in:
      assert user_name is not None
      menu.GetMenuItem(id_='user_name').SetText(user_name)
    menu.GetMenuItem(id_='user_name').SetDisplayed(logged_in)
    menu.GetMenuItem(id_='sign_in').SetDisplayed(not logged_in)
    menu.GetMenuItem(id_='sign_out').SetDisplayed(logged_in)

  def OnNotes(self, screen):
    self.GetStringVariable(id_='screen_label').SetValue('notes')
    return self._DisplayRecent(screen)

  def OnFavourites(self, screen):
    self.GetStringVariable(id_='screen_label').SetValue('favourites')
    return self._DisplayRecent(screen)

  def OnRecent(self, screen):
    self.GetStringVariable(id_='screen_label').SetValue('recent')
    return self._DisplayRecent(screen)
  
  def OnPlaces(self, screen):
    self.GetStringVariable(id_='screen_label').SetValue('places')
    return self._DisplayRecent(screen)

  def _DisplayRecent(self, screen):
    screen_label = self.GetVariable('screen_label')
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

  def _DisplayNotesByFunc(self, cmp_func, filter_func, screen):
    screen = fase.Screen()
    notes_layout = screen.AddLayout(orientation=fase.Layout.VERTICAL, scrollable=True)
    notes = notes_database.NotesDatabase.Get().GetUserNotes(self.GetUserId())
    if filter_func:
      notes = filter(notes, filter_func)
    for note in sorted(notes, cmp=cmp_func):
      note_layout = notes_layout.AddLayout(orientation=fase.Layout.VERTICAL)

      note_header_layout = note_layout.AddLayout(orientation=fase.Layout.HORIZONTAL)
      note_header_layout.AddLabel(label=note.header, font=2, sizable=fase.Label.FIT_OUTER_ELEMENT)
      note_header_layout.AddImage(image=('favourite.pnp' if note.favourite else 'favourite_non.pnp'))

      note_layout.AddLabel(label=note.text[:100])  # preview only

      datetime_text = datetime_util.GetDatetimeDiffStr(self.datetime, datetime.datetime.now())
      note_deails_layout = note_layout.AddLayout(orientation=fase.Layout.HORIZONTAL)
      note_deails_layout.AddLabel(
          label=datetime_text, font=0.75, aligh=fase.Text.LEFT, sizable=fase.Label.FIT_OUTER_ELEMENT)
      note_deails_layout.AddLabel(
          label=note.place_text, font=0.75, aligh=fase.Text.RIGHT, sizable=fase.Label.FIT_OUTER_ELEMENT)

      note_layout.SetOnClick(functools.partial(self.OnNote, note.note_id))

  def OnNew(self, screen):
    return self._DisplayNote(None, screen)

  def OnNote(self, note_id, screen):
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
    favourite_bool = screen.AddBooleanVariable(id_='favourite_bool', value=False)

    note = notes_database.NotesDatabase.Get().GetNote(note_id=note_id) if note_id is not None else None
    # If editing existing note.
    if note is not None:
      header_text.SetText(note.header)
      text_text.SetText(note.text)
      favourite_bool.SetValue(note.favourite)

    screen.AddNextStepButton(on_click=functools.partial(self.OnSaveNote, note_id))
    screen.AddPrevStepButton(on_click=self.OnCancelNote)

    context_menu = screen.AddContextMenu('Options')
    context_menu.AddMenuItem(text=('Remove from Favourites' if favourite_bool.GetValue() else 'Add to Favourites'),
                             on_click=functools.partial(self.OnReverseFavouriteNote, note_id),
                             icon=('favourite.pnp' if note is favourite_bool.GetValue() else 'favourite_non.pnp'))
    if note_id is not None:
      context_menu.AddMenuItem(
          text='Delete', icon='delete.pnp', on_click=functools.partial(self.OnDeleteNote, note_id))

  def OnSaveNote(self, note_id, screen):
    datetime_now = datetime.datetime.now()
    # If new note.
    if note_id is None:
      note_id_hash = hashlib.md5()
      note_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH))
      note_id_hash.update(self.GetUserId())
      note_id = note_id_hash.hexdigest()
    location = screen.GetUtilLocation()
    place_name = place_util.GetPlaceName(location)
    note = notes_model.Note(note_id=note_id,
                            header=screen.GetElemenet(id_='header_text').GetText(),
                            text=screen.GetElement(id_='text_text').GetText(),
                            datetime=datetime_now,
                            place_name=place_name,
                            favourite=screen.GetVariable('favourite_bool').GetValue())
    notes_database.NotesDatabase.Get().AddNote(note, overwrite=True)
    return self._DisplayRecent(screen)

  def OnCancelNote(self, screen):
    return self._DisplayRecent(screen)

  def OnReverseFavouriteNote(self, note_id, screen):
    favourite_bool = screen.GetBooleanVariable(id_='favourite_bool')
    favourite_bool.SetValue(not favourite_bool.GetValue())
    return screen

  def OnDeleteNote(self, note_id, screen):
    if note_id is not None:
      notes_database.NotesDatabase.Get().DeleteNote(note_id)
    return self._DisplayRecent(screen)
