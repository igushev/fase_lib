import datetime
import hashlib

import activation_code_generator
import sms_sender
import fase_database
import fase_model
import fase


class FaseSignInButton(fase.Button):

  def FaseOnClick(self, service, screen):
    activation_code_sent = service.GetIntVariable(id_='fase_sign_in_activation_code_str').GetValue()
    activation_code_entered = int(screen.GetLayout('enter_activation_layout_id').GetText('activation_code_text_id').GetText())
    if activation_code_sent != activation_code_entered:
      return service, fase.Popup('Wrong activation code!')
    
    on_sign_in_done = service.GetClassMethodVariable('fase_sign_in_on_sign_in_done_class_method').GetValue()
    screen_before_session_id = service.GetStringVariable('fase_sign_in_screen_before_session_id_str').GetValue() 
    session_id_signed_in = service.GetStringVariable(id_='fase_sign_in_session_id_signed_in_str').GetValue()
    # Delete service and screen current.
    session_id_current = service._session_id
    fase_database.FaseDatabaseInterface.Get().DeleteService(session_id=session_id_current)
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=session_id_current)

    if fase_database.FaseDatabaseInterface.Get().HasService(session_id=session_id_signed_in):
      # Delete screen before.
      fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)
      # Retrieve sign in service and call.
      service_signed_in = fase_database.FaseDatabaseInterface.Get().GetService(session_id=session_id_signed_in)
      screen_signed_in = on_sign_in_done(service_signed_in, user_id_before=service._session_id)
      return service_signed_in, screen_signed_in
    else:
      # Retrieve screen before and assign signed in session id.
      service._session_id = session_id_signed_in
      screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=screen_before_session_id)
      screen._session_id = session_id_signed_in
      fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)
      # Delete same object by old key.
      fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)
      return service, screen


class FaseSignOutButton(fase.Button):

  def FaseOnClick(self, service, screen):
    # Delete screen before.
    screen_before_session_id = service.GetStringVariable('fase_sign_in_screen_before_session_id_str').GetValue()
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)
    # Delete service and screen current.
    session_id_current = service._session_id
    fase_database.FaseDatabaseInterface.Get().DeleteService(session_id=session_id_current)
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=session_id_current)

    service_cls = fase.Service.service_cls
    service = service_cls()
    service._sessino_id = fase.GenerateSessionId()
    service._datetime_added = datetime.datetime.now()
    screen = service.OnStart()
    screen._session_id = service._session_id
    return service, screen


# TODO(igushev): fase_sign_in variables should be in separated better from services own variables.
class FaseSignIn(object):

  @staticmethod
  def StartSignIn(service, on_sign_in_done=None, skip_option=False, cancel_option=False):
    assert not fase_database.FaseDatabaseInterface.Get().HasUser(user_id=service._session_id)
    screen_before = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=service._session_id)
    screen_before_session_id = fase.GenerateSessionId()
    screen_before._session_id = screen_before_session_id
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen_before)
    service.AddClassMethodVariable('fase_sign_in_on_sign_in_done_class_method', on_sign_in_done)
    service.AddStringVariable('fase_sign_in_screen_before_session_id_str', screen_before_session_id)

    screen = fase.Screen()
    sign_in_layout = screen.AddLayout(id_='sign_in_layout_id', orientation=fase.Layout.VERTICAL)
    sign_in_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=FaseSignIn.OnSignInOption)
    sign_in_layout.AddButton(id_='sign_up_button_id', text='Sign Up', on_click=FaseSignIn.OnSignUpOption)
    if skip_option:
      sign_in_layout.AddButton(id_='skip_button_id', text='Skip', on_click=FaseSignIn.OnSkipCancelOption)
    elif cancel_option:
      screen.AddPrevStepButton(on_click=FaseSignIn.OnSkipCancelOption)
    return screen

  @staticmethod
  def OnSignInOption(service, screen, element):
    screen = fase.Screen()
    sign_in_layout = screen.AddLayout(id_='sign_in_layout_id', orientation=fase.Layout.VERTICAL)
    sign_in_layout.AddText(id_='phone_number_text_id', hint='Phone Number')
    sign_in_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=FaseSignIn.OnSignInEnteredData)
    screen.AddPrevStepButton(on_click=FaseSignIn.StartSignIn)
    return screen

  @staticmethod
  def OnSignInEnteredData(service, screen, element):
    sign_in_layout = screen.GetElement(id_='sign_in_layout_id')
    phone_number = sign_in_layout.GetText(id_='phone_number_text_id').GetText()
    phone_number_user_list = fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number)
    assert len(phone_number_user_list) == 1
    user = phone_number_user_list[0]
    if not user:
      return fase.Popup('User with such phone number has not been found!')
    return FaseSignIn._OnEnteredData(service, phone_number, user.user_id)

  @staticmethod
  def OnSignUpOption(service, screen, element):
    screen = fase.Screen()
    sign_up_layout = screen.AddLayout(id_='sign_up_layout_id', orientation=fase.Layout.VERTICAL)
    sign_up_layout.AddText(id_='phone_number_text_id', hint='Phone Number')
    sign_up_layout.AddText(id_='first_name_text_id', hint='First Name')
    sign_up_layout.AddText(id_='last_name_text_id', hint='Last Name')
    sign_up_layout.AddButton(id_='sign_up_button_id', text='Sign In', on_click=FaseSignIn.OnSignUpEnteredData)
    screen.AddPrevStepButton(on_click=FaseSignIn.StartSignIn)
    return screen
    
  @staticmethod
  def OnSignUpEnteredData(service, screen, element):
    sign_up_layout = screen.GetElement('sign_up_layout_id')
    phone_number = sign_up_layout.GetText(id_='phone_number_text_id').GetText()
    if fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number):
      return fase.Popup('User with such phone number is already registered!')

    datetime_now = datetime.datetime.now()
    user_id_hash = hashlib.md5()
    user_id_hash.update(datetime_now.strftime(fase.DATETIME_FORMAT_HASH))
    user_id_hash.update(phone_number)
    user_id = user_id_hash.hexdigest()
    
    user = fase_model.User(user_id=user_id,
                           phone_number=sign_up_layout.GetText(id_='phone_number_text_id').GetText(),
                           first_name=sign_up_layout.GetText(id_='first_name_text_id').GetText(),
                           last_name=sign_up_layout.GetText(id_='last_name_text_id').GetText(),
                           datetime_added=datetime_now)
    fase_database.FaseDatabaseInterface.Get().AddUser(user)
    return FaseSignIn._OnEnteredData(service, phone_number, user_id)

  @staticmethod
  def _OnEnteredData(service, phone_number, user_id):
    activation_code = activation_code_generator.ActivationCodeGenerator.Get().Generate()
    sms_sender.SMSSender.Get().SendActivationCode(phone_number, activation_code)
    screen = fase.Screen()
    enter_activation_layout = screen.AddLayout(id_='enter_activation_layout_id', orientation=fase.Layout.VERTICAL)
    enter_activation_layout.AddText(id_='activation_code_text_id', hint='Activation Code')
    enter_activation_layout.AddElement(id_='send_button_id', element=FaseSignInButton(text='Send'))
    service.AddStringVariable(id_='fase_sign_in_session_id_signed_in_str', value=user_id)
    service.AddIntVariable(id_='fase_sign_in_activation_code_str', value=activation_code)
    screen.AddPrevStepButton(on_click=FaseSignIn.StartSignIn)
    return screen

  @staticmethod
  def StartSignOut(service, cancel_option=False):
    assert fase_database.FaseDatabaseInterface.Get().HasUser(user_id=service._session_id)
    screen_before = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=service._session_id)
    screen_before_session_id = fase.GenerateSessionId()
    screen_before._session_id = screen_before_session_id
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen_before)
    service.AddStringVariable('fase_sign_in_screen_before_session_id_str', screen_before_session_id)

    screen = fase.Screen()
    sign_out_layout = screen.AddLayout(id_='sign_out_layout_id', orientation=fase.Layout.VERTICAL)
    sign_out_layout.AddElement(id_='sign_out_button_id', element=FaseSignOutButton(text='Sign Out'))
    if cancel_option:
      screen.AddPrevStepButton(on_click=FaseSignIn.OnSkipCancelOption)
    return screen

  @staticmethod
  def OnSkipCancelOption(service, screen, element):
    screen_before_session_id = service.GetStringVariable('fase_sign_in_screen_before_session_id_str').GetValue() 
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=screen_before_session_id)
    screen._session_id = service._session_id
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)
    # Delete same object by old key.
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)
    return screen