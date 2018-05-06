import datetime

from server_util import phone_number_verifier

from fase import fase
from fase import fase_pusher
from fase import fase_sign_in

from karmacounter_fase import client as kc_client
from karmacounter_fase import data as kc_data


DEVICE_TYPE = 'Fase'
APP_NAME = 'KarmaCounter'

GET_USER_SESSION_CODE = 'KarmaCounterGetUserSession'
SCORE_NOT_SELECTED = 'Please select a score!'
PHONE_IS_INVALID = 'Phone number format is invalid!'
PHONE_NO_COUNTRY_CODE = 'Phone number country code could not be inferred! Please try to add explicitly!'
MIN_AGE_YEARS = 13

ADDED_EVENT_TO_USER_MSG = '%s has added you a new event'
ADDED_EVENT_TO_WITNESS_MSG = '%s has asked you to witness an event' 
ACCEPTED_EVENT_TO_USER_MSG = '%s accepted an event you asked them to witness'
ACCEPTED_EVENT_TO_WITNESS_MSG = '%s accepted an event you added to them'
REJECTED_EVENT_TO_USER_MSG = '%s rejected an event you asked them to witness'
REJECTED_EVENT_TO_WITNESS_MSG = '%s rejected an event you added to them'
DELETED_EVENT_ADDED_BY_USER_MSG = '%s deleted an event they asked you to witness'
DELETED_EVENT_ADDED_BY_WITNESS_MSG = '%s deleted an event you added to them'


def _ErrorAlert(service, message, on_click):
  screen = fase.Screen(service)
  alert = screen.AddAlert(message)
  alert.AddButton(text="OK", on_click=on_click)
  return screen


class KarmaCounter(fase.Service):

  @staticmethod
  def GetServiceId():
    return APP_NAME

  def _PushNotification(self, phone_number, message):
    user_id = fase_sign_in.GetUserIdByPhoneNumber(phone_number)
    # Here user_id might be None because of backwards compatibility, when user might has registered using old Frontend
    # and Fase Frontend does not has their information.
    if user_id is None:
      return
    fase_pusher.Push(user_id, APP_NAME, message)

  def OnStart(self):
    self.AddStringVariable(id_='screen_label_str', value='dashboard')
    min_date_of_birth = datetime.datetime.utcnow() - datetime.timedelta(days=MIN_AGE_YEARS*365)
    return fase_sign_in.StartSignIn(
        self, on_done=KarmaCounter.OnSignInDone,
        request_user_data=fase.RequestUserData(date_of_birth=True, home_city=True, min_date_of_birth=min_date_of_birth))

  def OnSignInDone(self, user_id_before=None):
    new_user = kc_data.NewUser(phone_number=self.GetUser().GetPhoneNumber(),
                               first_name=self.GetUser().GetFirstName(),
                               last_name=self.GetUser().GetLastName(),
                               city=kc_data.CommonCity(google_place_id=self.GetUser().GetHomeCity().GetGooglePlaceId(),
                                                       city=self.GetUser().GetHomeCity().GetCity(),
                                                       state=self.GetUser().GetHomeCity().GetState(),
                                                       country=self.GetUser().GetHomeCity().GetCountry()),
                               date_of_birth=self.GetUser().GetDateOfBirth(),
                               device=kc_data.Device(device_type=DEVICE_TYPE,
                                                     device_token=self.GetUserId()),
                               locale=self.GetUser().GetLocale(),
                               code=GET_USER_SESSION_CODE)
    session_info = kc_client.KarmaCounterClient.Get().GetUserSession(new_user)
    if not self.HasStringVariable(id_='session_id_str'):
      self.AddStringVariable(id_='session_id_str', value=session_info.session_id)
    return self.DisplayCurrentScreen(None, None)

  def OnUpdate(self):
    if self.IfSignedIn():
      return self.OnSignInDone()
    else:
      return self.OnStart()

  def DisplayCurrentScreen(self, screen, element):
    screen_label = self.GetStringVariable(id_='screen_label_str').GetValue()
    if screen_label == 'dashboard':
      return self.DisplayDashboard(screen, element)
    elif screen_label == 'your_events':
      return self.DisplayYourEvents(screen, element)
    elif screen_label == 'your_friends_events':
      return self.DisplayYourFriendsEvents(screen, element)
    elif screen_label == 'statistics_by_cities':
      return self.DisplayStatisticsByCities(screen, element)
    else:
      raise AssertionError(screen_label)

  def OnDisplayDashboard(self, screen, element):
    self.GetStringVariable(id_='screen_label_str').SetValue('dashboard')
    return self.DisplayDashboard(screen, element)

  def OnDisplayYourEvents(self, screen, element):
    self.GetStringVariable(id_='screen_label_str').SetValue('your_events')
    return self.DisplayYourEvents(screen, element)

  def OnDisplayYourFriendsEvents(self, screen, element):
    self.GetStringVariable(id_='screen_label_str').SetValue('your_friends_events')
    return self.DisplayYourFriendsEvents(screen, element)

  def OnDisplayStatisticsByCities(self, screen, element):
    self.GetStringVariable(id_='screen_label_str').SetValue('statistics_by_cities')
    return self.DisplayStatisticsByCities(screen, element)

  def OnSignOut(self, screen, element):
    return fase_sign_in.StartSignOut(self, on_cancel=KarmaCounter.OnSignOutCancel)

  def OnSignOutCancel(self):
    return self.DisplayCurrentScreen(None, None)

  def _AddButtons(self, screen):
    navigation = screen.AddNavigation()
    navigation.AddButton(text='Dashboard', image=fase.Image(filename='images/dashboard_@.png'),
                         on_click=KarmaCounter.OnDisplayDashboard)
    navigation.AddButton(text='Your Events', image=fase.Image(filename='images/your_events_@.png'),
                         on_click=KarmaCounter.OnDisplayYourEvents)
    navigation.AddButton(text='Your Friends Events', image=fase.Image(filename='images/your_friends_events_@.png'),
                         on_click=KarmaCounter.OnDisplayYourFriendsEvents)
    navigation.AddButton(text='Statistics by Cities', image=fase.Image(filename='images/statistics_by_cities_@.png'),
                         on_click=KarmaCounter.OnDisplayStatisticsByCities)
    navigation.AddButton(text='Sign Out', image=fase.Image(filename='images/sign_out_@.png'),
                         on_click=KarmaCounter.OnSignOut)
    main_button = screen.AddMainButton(text='Add Event', image=fase.Image(filename='images/add_event_@.png'))
    main_button_context_menu = main_button.AddContextMenu()
    main_button_context_menu.AddMenuItem(text='Add Event to Yourself', on_click=KarmaCounter.OnAddUserEvent)
    main_button_context_menu.AddMenuItem(text='Add Event to Friend', on_click=KarmaCounter.OnAddOtherUserEvent)

  def DisplayDashboard(self, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    starting_page = kc_client.KarmaCounterClient.Get().GetStartingPage(session_info)
    screen = fase.Screen(self)
    screen.SetTitle('Dashboard')
    dashboard_frame = screen.AddFrame(orientation=fase.Frame.VERTICAL)
    dashboard_frame.AddLabel(text='Score', size=fase.Label.MAX)
    dashboard_frame.AddLabel(text=str(starting_page.user.score), font=1.5, size=fase.Label.MAX)
    self._AddButtons(screen)
    return screen

  def _AddUserEvent(self, screen, element, users_own=True):
    screen = fase.Screen(self)
    users_own = self.GetBoolVariable(id_='adding_users_own_bool').GetValue()
    screen.SetTitle('To Yourself' if users_own else 'To a Friend')
    screen.AddSelect(id_='score_select', items=['-10', '-3', '-1', '0', '1', '3', '10'], hint='Score',
                     align=fase.Select.LEFT)
    screen.AddContactPicker(id_='friend_contact_picker', hint='Friend', on_pick=KarmaCounter.OnFriendPick)
    screen.AddSwitch(id_='invite_switch', value=False, text='Invite Friend', align=fase.Switch.LEFT)
    screen.AddText(id_='description_text', hint='Description')
    screen.AddNextStepButton(text='Add', on_click=KarmaCounter.OnAddUserEventEnteredData)
    screen.AddPrevStepButton(text='Cancel', on_click=KarmaCounter.OnAddUserEventCancel)
    self.OnFriendPick(screen, None)
    return screen

  def OnFriendPick(self, screen, element):
    friend_contact_picker = screen.GetContactPicker(id_='friend_contact_picker')
    invite_switch = screen.GetSwitch(id_='invite_switch')
    if friend_contact_picker.GetContact() and friend_contact_picker.GetContact().GetPhoneNumber():

      phone_number = friend_contact_picker.GetContact().GetPhoneNumber()
      try:
        phone_number = phone_number_verifier.Format(phone_number, self.GetUser().GetLocale().GetCountryCode())
      except phone_number_verifier.NoCountryCodeException:
        return _ErrorAlert(self, message=PHONE_NO_COUNTRY_CODE, on_click=KarmaCounter._AddUserEvent)
      except phone_number_verifier.InvalidPhoneNumberException:
        return _ErrorAlert(self, message=PHONE_IS_INVALID, on_click=KarmaCounter._AddUserEvent)

      request_registered_users = kc_data.RequestRegisteredUsers(phone_number_list=[phone_number])
      session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
      registered_users = kc_client.KarmaCounterClient.Get().GetRegisteredUsers(request_registered_users, session_info)
      if registered_users.users:
        friend_contact_picker.GetContact().SetDisplayName(registered_users.users[0].display_name)
        invite_switch.SetDisplayed(False)
      else:
        invite_switch.SetDisplayed(True)
    else:
      invite_switch.SetDisplayed(False)
    return screen

  def OnAddUserEvent(self, screen, element):
    if self.HasBoolVariable(id_='adding_users_own_bool'):
      self.PopBoolVariable(id_='adding_users_own_bool')
    self.AddBoolVariable(id_='adding_users_own_bool', value=True)
    return self._AddUserEvent(screen, element)

  def OnAddOtherUserEvent(self, screen, element):
    if self.HasBoolVariable(id_='adding_users_own_bool'):
      self.PopBoolVariable(id_='adding_users_own_bool')
    self.AddBoolVariable(id_='adding_users_own_bool', value=False)
    return self._AddUserEvent(screen, element)

  def OnAddUserEventEnteredData(self, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    score_text = screen.GetSelect(id_='score_select').GetValue()
    if not score_text:
      return _ErrorAlert(self, message=SCORE_NOT_SELECTED, on_click=KarmaCounter._AddUserEvent)
    score = int(score_text)
    if self.GetBoolVariable(id_='adding_users_own_bool').GetValue():
      witness_phone_number = (screen.GetContactPicker(id_='friend_contact_picker').GetContact().GetPhoneNumber()
                              if screen.GetContactPicker(id_='friend_contact_picker').GetContact() is not None else
                              None)
      if witness_phone_number is not None:
        witness_phone_number = (
            phone_number_verifier.Format(witness_phone_number, self.GetUser().GetLocale().GetCountryCode()))
      witness_display_name = (screen.GetContactPicker(id_='friend_contact_picker').GetContact().GetDisplayName()
                              if screen.GetContactPicker(id_='friend_contact_picker').GetContact() is not None else
                              None)
      new_user_event = kc_data.NewUserEvent(
          score=score,
          description=screen.GetText(id_='description_text').GetText(),
          witness_phone_number=witness_phone_number,
          witness_display_name=witness_display_name,
          invite_witness=screen.GetSwitch(id_='invite_switch').GetValue())
      kc_client.KarmaCounterClient.Get().AddUserEvent(new_user_event, session_info)
      self._PushNotification(witness_phone_number, ADDED_EVENT_TO_WITNESS_MSG % self.GetUser().DisplayName())
    else:
      phone_number = screen.GetContactPicker(id_='friend_contact_picker').GetContact().GetPhoneNumber()
      phone_number = phone_number_verifier.Format(phone_number, self.GetUser().GetLocale().GetCountryCode())
      other_user_display_name = screen.GetContactPicker(id_='friend_contact_picker').GetContact().GetDisplayName()
      new_other_user_event = kc_data.NewOtherUserEvent(
          score=score,
          description=screen.GetText(id_='description_text').GetText(),
          phone_number=phone_number,
          other_user_display_name=other_user_display_name,
          invite_other_user=screen.GetSwitch(id_='invite_switch').GetValue())
      kc_client.KarmaCounterClient.Get().AddOtherUserEvent(new_other_user_event, session_info)
      self._PushNotification(phone_number, ADDED_EVENT_TO_USER_MSG % self.GetUser().DisplayName())
    self.PopBoolVariable(id_='adding_users_own_bool')
    return self.DisplayCurrentScreen(screen, element)

  def OnAddUserEventCancel(self, screen, element):
    self.PopBoolVariable(id_='adding_users_own_bool')
    return self.DisplayCurrentScreen(screen, element)

  def _DisplayEvents(self, screen, element, users_own=True):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    user_events = (kc_client.KarmaCounterClient.Get().GetUserEvents(session_info) if users_own else
                   kc_client.KarmaCounterClient.Get().GetOtherUserEvents(session_info))
    screen = fase.Screen(self)
    screen.SetTitle('Your Events' if users_own else 'Your Friend\'s Events')
    screen.SetScrollable(True)
    for user_event in user_events.events:
      user_event_frame = screen.AddFrame(
          id_='user_event_frame_%s' % user_event.event_id, orientation=fase.Frame.VERTICAL, border=True)
      user_event_header_frame = user_event_frame.AddFrame(
          id_='user_event_header_frame', orientation=fase.Frame.HORIZONTAL)
      user_event_header_frame.AddLabel(
          id_='user_event_score_label', text=str(user_event.score), font=1.5)
      if users_own:
        friend_display_name = user_event.witness.display_name if user_event.witness is not None else None
        friend_phone_number = user_event.witness.phone_number if user_event.witness is not None else None
        user_event_header_frame.AddLabel(
            id_='user_event_friend_display_name_label', text=friend_display_name, size=fase.Label.MAX)
      else:
        friend_phone_number = user_event.user.phone_number
        user_event_header_frame.AddLabel(
            id_='user_event_friend_display_name_label', text=user_event.user.display_name, size=fase.Label.MAX)
      user_event_header_frame.AddLabel(text=user_event.display_datetime)
      user_event_frame.AddLabel(text=user_event.description, align=fase.Label.LEFT)
      user_event_frame.AddLabel(text=user_event.display_status, align=fase.Label.LEFT, font=0.75)
      user_event_button_frame = user_event_frame.AddFrame(orientation=fase.Frame.HORIZONTAL)
      user_event_button_frame.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Label.MAX)

      if user_event.verification_status == kc_data.VerificationStatus.pending:
        if (users_own and not user_event.self_added) or (not users_own and user_event.self_added):
          accept_button = user_event_button_frame.AddButton(
              id_='user_event_accept_button', text='Accept', on_click=KarmaCounter.OnAccept)
          accept_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)
          accept_button.AddStringVariable(id_='friend_phone_number_str', value=friend_phone_number)
          reject_button = user_event_button_frame.AddButton(
              id_='user_event_reject_button', text='Reject', on_click=KarmaCounter.OnReject)
          reject_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)
          reject_button.AddStringVariable(id_='friend_phone_number_str', value=friend_phone_number)

      user_event_context_button = user_event_button_frame.AddButton(text='...')
      user_event_context_menu = user_event_context_button.AddContextMenu()
      report_abuse_button = user_event_context_menu.AddMenuItem(
          id_='report_abuse_menu_item', text='Report Abuse', on_click=KarmaCounter.OnReportAbuse)
      report_abuse_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)
      report_spam_button = user_event_context_menu.AddMenuItem(
          id_='report_spam_menu_item', text='Report Spam', on_click=KarmaCounter.OnReportSpam)
      report_spam_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)
      block_user_button = user_event_context_menu.AddMenuItem(
          id_='block_user_menu_item', text='Block User', on_click=KarmaCounter.OnBlockUser)
      block_user_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)

      if users_own:
        delete_button = user_event_context_menu.AddMenuItem(
            id_='delete_menu_item', text='Delete', on_click=KarmaCounter.OnDelete)
        delete_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)
        delete_button.AddStringVariable(id_='friend_phone_number_str', value=friend_phone_number)

    self._AddButtons(screen)
    return screen

  def DisplayYourEvents(self, screen, element):
    return self._DisplayEvents(screen, element, users_own=True)
  
  def DisplayYourFriendsEvents(self, screen, element):
    return self._DisplayEvents(screen, element, users_own=False)

  def _SendUserEventInfo(self, func, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    user_event_info = kc_data.UserEventInfo(event_id=element.GetStringVariable(id_='user_event_id_str').GetValue())
    func(user_event_info, session_info)
    return self.DisplayCurrentScreen(screen, element)

  def _PushNotificationUserEventAction(self, element, users_own_message_template, not_users_own_message_template):
    friend_phone_number = element.GetStringVariable(id_='friend_phone_number_str').GetValue()
    if not friend_phone_number:
      return
    screen_label = self.GetStringVariable(id_='screen_label_str').GetValue()
    if screen_label == 'your_events':
      users_own = True
    elif screen_label == 'your_friends_events':
      users_own = False
    else:
      return
    if users_own:
      self._PushNotification(friend_phone_number, users_own_message_template % self.GetUser().DisplayName())
    else:
      self._PushNotification(friend_phone_number, not_users_own_message_template % self.GetUser().DisplayName())

  def OnAccept(self, screen, element):
    screen = self._SendUserEventInfo(kc_client.KarmaCounterClient.Get().AcceptUserEvent, screen, element)
    self._PushNotificationUserEventAction(
        element,
        users_own_message_template=ACCEPTED_EVENT_TO_WITNESS_MSG,
        not_users_own_message_template=ACCEPTED_EVENT_TO_USER_MSG)
    return screen

  def OnReject(self, screen, element):
    screen = self._SendUserEventInfo(kc_client.KarmaCounterClient.Get().RejectUserEvent, screen, element)
    self._PushNotificationUserEventAction(
        element,
        users_own_message_template=REJECTED_EVENT_TO_WITNESS_MSG,
        not_users_own_message_template=REJECTED_EVENT_TO_USER_MSG)
    return screen

  def OnDelete(self, screen, element):
    screen = self._SendUserEventInfo(kc_client.KarmaCounterClient.Get().DeleteUserEvent, screen, element)
    self._PushNotificationUserEventAction(
        element,
        users_own_message_template=DELETED_EVENT_ADDED_BY_WITNESS_MSG,
        not_users_own_message_template=DELETED_EVENT_ADDED_BY_USER_MSG)
    return screen

  def OnReportAbuse(self, screen, element):
    return self._SendUserEventInfo(kc_client.KarmaCounterClient.Get().ReportAbuse, screen, element)

  def OnReportSpam(self, screen, element):
    return self._SendUserEventInfo(kc_client.KarmaCounterClient.Get().ReportSpam, screen, element)

  def OnBlockUser(self, screen, element):
    return self._SendUserEventInfo(kc_client.KarmaCounterClient.Get().BlockUser, screen, element)

  def _DisplayCitiesStatistics(self, frame, cities_statistics):
    for city_statistics in cities_statistics:
      city_frame = frame.AddFrame(orientation=fase.Frame.HORIZONTAL)
      city_frame.AddLabel(text=city_statistics.display_name)
      city_frame.AddFrame(size=fase.Frame.MAX, orientation=fase.Frame.HORIZONTAL)
      city_frame.AddLabel(text=city_statistics.display_score)

  def DisplayStatisticsByCities(self, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    cities_statistics_top_bottom = kc_client.KarmaCounterClient.Get().CitiesStatisticsTopBottom(session_info)
    screen = fase.Screen(self)
    screen.SetTitle('Statistics by Cities')
    screen.AddLabel(text='Cities With Highest Score')
    top_frame = screen.AddFrame(orientation=fase.Frame.VERTICAL)
    self._DisplayCitiesStatistics(top_frame, cities_statistics_top_bottom.external_cities_statistics_top)

    screen.AddLabel(text='Cities With Lowest Score')
    bottom_frame = screen.AddFrame(orientation=fase.Frame.VERTICAL)
    self._DisplayCitiesStatistics(bottom_frame, cities_statistics_top_bottom.external_cities_statistics_bottom)
    self._AddButtons(screen)
    return screen

  
fase.Service.RegisterService(KarmaCounter)
