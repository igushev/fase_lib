import fase
import fase_sign_in

from KarmaCounter import client as kc_client
from KarmaCounter import data as kc_data


class KarmaCounter(fase.Service):

  @staticmethod
  def GetServiceId():
    return 'KarmaCounter'

  def OnStart(self):
    self.AddStringVariable(id_='screen_label_str', value='dashboard')
    return fase_sign_in.StartSignIn(self, on_done=KarmaCounter.OnSignInDone)

  def OnSignInDone(self, user_id_before=None):
    new_user = kc_data.NewUser(phone_number=self.GetUserPhoneNumber(),
                               first_name=self.GetUserName(),
                               last_name=None,
                               city=kc_data.CommonCity(google_place_id='fake_id',
                                                       city='New York City',
                                                       state=None,
                                                       country='US'),
                               date_of_birth=None,
                               device=None,
                               locale=None)
    session_info = kc_client.GetUserSession(new_user)
    if not self.HasStringVariable(id_='session_id_str'):
      self.AddStringVariable(id_='session_id_str', value=session_info.session_id)
    return self.DisplayCurrentScreen(None, None)

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
    main_menu = screen.AddMainMenu()
    main_menu.AddMenuItem(id_='user_name_menu_item', text=self.GetUserName())
    main_menu.AddMenuItem(id_='sign_out_menu_item', text='Sign Out', on_click=KarmaCounter.OnSignOut)
    button_bar = screen.AddButtonBar()
    button_bar.AddButton(id_='dashboard_button', text='Dashboard', on_click=KarmaCounter.OnDisplayDashboard)
    button_bar.AddButton(id_='your_events_button', text='Your Events', on_click=KarmaCounter.OnDisplayYourEvents)
    button_bar.AddButton(
        id_='your_friends_events_button', text='Your Friends Events', on_click=KarmaCounter.OnDisplayYourFriendsEvents)
    button_bar.AddButton(
        id_='statistics_by_cities_button', text='Statistics by Cities',
        on_click=KarmaCounter.OnDisplayStatisticsByCities)
    main_button_context_menu = fase.Menu()
    main_button_context_menu.AddMenuItem(
        id_='add_event_to_yourself', text='Add Event to Yourself', on_click=KarmaCounter.OnAddUserEvent)
    main_button_context_menu.AddMenuItem(
        id_='add_event_to_friend', text='Add Event to Friend', on_click=KarmaCounter.OnAddOtherUserEvent)
    screen.AddMainButton(text='Add Event', context_menu=main_button_context_menu)

  def DisplayDashboard(self, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    starting_page = kc_client.GetStartingPage(session_info)
    screen = fase.Screen(self)
    screen.SetTitle('Dashboard')
    dashboard_layout = screen.AddLayout(id_='dashboard_layout', orientation=fase.Layout.VERTICAL)
    dashboard_layout.AddLabel(id_='score_title_label', label='Score', size=fase.Label.MAX)
    dashboard_layout.AddLabel(id_='score_label', label=str(starting_page.user.score), font=3.0, size=fase.Label.MAX)
    self._AddButtons(screen)
    return screen

  def _AddUserEvent(self, screen, element, users_own=True):
    screen = fase.Screen(self)
    screen.SetTitle('To Yourself' if users_own else 'To a Friend')
    screen.AddBoolVariable(id_='adding_users_own_bool', value=users_own)
    screen.AddText(id_='score_text', hint='Score')
    screen.AddContactPicker(id_='friend_contact_picker', hint='Friend', on_pick=KarmaCounter.OnFriendPick)
    screen.AddSwitch(id_='invite_switch', value=False, text='Invite Friend', alight=fase.Switch.LEFT)
    screen.AddText(id_='description_text', hint='Description')
    screen.AddNextStepButton(text='Add', on_click=KarmaCounter.OnAddUserEventEnteredData)
    screen.AddPrevStepButton(text='Cancel', on_click=KarmaCounter.DisplayCurrentScreen)
    self.OnFriendPick(screen, None)
    return screen

  def OnFriendPick(self, screen, element):
    friend_contact_picker = screen.GetContactPicker(id_='friend_contact_picker')
    invite_switch = screen.GetSwitch(id_='invite_switch')
    if friend_contact_picker.GetPhoneNumber():
      request_registered_users = (
          kc_data.RequestRegisteredUsers(phone_number_list=[friend_contact_picker.GetPhoneNumber()]))
      session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
      registered_users = kc_client.GetRegisteredUsers(request_registered_users, session_info)
      if registered_users.users:
        friend_contact_picker.SetDisplayName(registered_users.users[0].display_name)
        invite_switch.SetDisplayed(False)
      else:
        invite_switch.SetDisplayed(True)
    else:
      invite_switch.SetDisplayed(False)
    return screen

  def OnAddUserEvent(self, screen, element):
    return self._AddUserEvent(screen, element, users_own=True)

  def OnAddOtherUserEvent(self, screen, element):
    return self._AddUserEvent(screen, element, users_own=False)

  def OnAddUserEventEnteredData(self, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    if screen.GetBoolVariable(id_='adding_users_own_bool').GetValue():
      new_user_event = kc_data.NewUserEvent(
          score=int(screen.GetText(id_='score_text').GetText()),
          description=screen.GetText(id_='description_text').GetText(),
          witness_phone_number=screen.GetContactPicker(id_='friend_contact_picker').GetPhoneNumber(),
          witness_display_name=screen.GetContactPicker(id_='friend_contact_picker').GetDisplayName(),
          invite_witness=screen.GetSwitch(id_='invite_switch').GetValue())
      kc_client.AddUserEvent(new_user_event, session_info)
    else:
      new_other_user_event = kc_data.NewOtherUserEvent(
          score=int(screen.GetText(id_='score_text').GetText()),
          description=screen.GetText(id_='description_text').GetText(),
          phone_number=screen.GetContactPicker(id_='friend_contact_picker').GetPhoneNumber(),
          other_user_display_name=screen.GetContactPicker(id_='friend_contact_picker').GetDisplayName(),
          invite_other_user=screen.GetSwitch(id_='invite_switch').GetValue())
      kc_client.AddOtherUserEvent(new_other_user_event, session_info)
    return self.DisplayCurrentScreen(screen, element)

  def _DisplayEvents(self, screen, element, users_own=True):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    user_events = kc_client.GetUserEvents(session_info) if users_own else kc_client.GetOtherUserEvents(session_info)
    screen = fase.Screen(self)
    screen.SetTitle('Your Events' if users_own else 'Your Friend\'s Events')
    screen.SetScrollable(True)
    for user_event in user_events.events:
      user_event_layout = screen.AddLayout(
          id_='user_event_layout_%s' % user_event.event_id, orientation=fase.Layout.VERTICAL, border=True)
      user_event_header_layout = user_event_layout.AddLayout(
          id_='user_event_header_layout', orientation=fase.Layout.HORIZONTAL)
      user_event_header_layout.AddLabel(
          id_='user_event_score_label', label=str(user_event.score), font=1.5)
      if users_own:
        friend_name = user_event.witness.display_name if user_event.witness is not None else None
        user_event_header_layout.AddLabel(id_='user_event_friend_name_label', label=friend_name, size=fase.Label.MAX)
      else:
        user_event_header_layout.AddLabel(
            id_='user_event_friend_name_label', label=user_event.user.display_name, size=fase.Label.MAX)
      user_event_header_layout.AddLabel(id_='user_event_date_label', label=user_event.display_datetime)
      user_event_layout.AddLabel(
          id_='user_event_description_label', label=user_event.description, alight=fase.Label.LEFT)
      user_event_layout.AddLabel(id_='user_event_status_label', label=user_event.display_status, alight=fase.Label.LEFT)
      user_event_button_layout = user_event_layout.AddLayout(
          id_='user_event_button_layout', orientation=fase.Layout.HORIZONTAL)
      user_event_button_layout.AddLayout(
          id_='button_emtpy_layout', orientation=fase.Layout.HORIZONTAL, size=fase.Label.MAX)

      if user_event.verification_status == kc_data.VerificationStatus.pending:
        if (users_own and not user_event.self_added) or (not users_own and user_event.self_added):
          accept_button = user_event_button_layout.AddButton(
              id_='user_event_accept_button', text='Accept', on_click=KarmaCounter.OnAccept)
          accept_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)
          reject_button = user_event_button_layout.AddButton(
              id_='user_event_reject_button', text='Reject', on_click=KarmaCounter.OnReject)
          reject_button.AddStringVariable(id_='user_event_id_str', value=user_event.event_id)

      user_event_context_menu = fase.Menu()
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
      user_event_button_layout.AddButton(id_='user_event_context_menu_button', context_menu=user_event_context_menu)

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

  def OnAccept(self, screen, element):
    return self._SendUserEventInfo(kc_client.AcceptUserEvent, screen, element)

  def OnReject(self, screen, element):
    return self._SendUserEventInfo(kc_client.RejectUserEvent, screen, element)

  def OnDelete(self, screen, element):
    return self._SendUserEventInfo(kc_client.DeleteUserEvent, screen, element)

  def OnReportAbuse(self, screen, element):
    return self._SendUserEventInfo(kc_client.ReportAbuse, screen, element)

  def OnReportSpam(self, screen, element):
    return self._SendUserEventInfo(kc_client.ReportSpam, screen, element)

  def OnBlockUser(self, screen, element):
    return self._SendUserEventInfo(kc_client.BlockUser, screen, element)

  def _DisplayCitiesStatistics(self, layout, cities_statistics):
    for i, city_statistics in enumerate(cities_statistics):
      city_layout = layout.AddLayout(id_='city_layout_%d' % i, orientation=fase.Layout.HORIZONTAL)
      city_layout.AddLabel(id_='city_name_label', label=city_statistics.display_name)
      city_layout.AddLabel(id_='city_score_label', label=city_statistics.display_score)

  def DisplayStatisticsByCities(self, screen, element):
    session_info = kc_data.SessionInfo(session_id=self.GetStringVariable(id_='session_id_str').GetValue())
    cities_statistics_top_bottom = kc_client.CitiesStatisticsTopBottom(session_info)
    screen = fase.Screen(self)
    screen.AddLabel(id_='top_label', label='Cities With Highest Score')
    top_layout = screen.AddLayout(id_='top_layout', orientation=fase.Layout.VERTICAL)
    self._DisplayCitiesStatistics(top_layout, cities_statistics_top_bottom.external_cities_statistics_top)

    screen.AddLabel(id_='bottom_label', label='Cities With Lowest Score')
    bottom_layout = screen.AddLayout(id_='bottom_layout', orientation=fase.Layout.VERTICAL)
    self._DisplayCitiesStatistics(bottom_layout, cities_statistics_top_bottom.external_cities_statistics_bottom)
    self._AddButtons(screen)
    return screen

  
fase.Service.RegisterService(KarmaCounter)
