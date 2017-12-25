import datetime
import hashlib

import activation_code_generator
import sms_sender
import fase_database
import fase_model
import fase
import json_util


@json_util.JSONDecorator({})
class FaseSignInButton(fase.Button):

  def FaseOnClick(self, service, screen):
    activation_code_sent = service.PopIntVariable(id_='fase_sign_in_activation_code_int').GetValue()
    activation_code_entered = int(
        screen.GetLayout(id_='enter_activation_layout_id').GetText(id_='activation_code_text_id').GetText())
    if activation_code_sent != activation_code_entered:
      screen.AddPopup('Wrong activation code!')
      return service, screen

    on_sign_in_done = service.PopFunctionVariable(id_='fase_sign_in_on_sign_in_done_class_method').GetValue()
    screen_before_session_id = service.PopStringVariable(id_='fase_sign_in_screen_before_session_id_str').GetValue() 
    session_id_signed_in = service.PopStringVariable(id_='fase_sign_in_session_id_signed_in_str').GetValue()
    # Delete service and screen current.
    session_id_current = service.GetSessionId()
    fase_database.FaseDatabaseInterface.Get().DeleteService(session_id=session_id_current)
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=session_id_current)
    # Delete screen before.
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)

    service_signed_in = fase_database.FaseDatabaseInterface.Get().GetService(session_id=session_id_signed_in)
    if service_signed_in:
      # Retrieve sign in service and call.
      screen_signed_in = on_sign_in_done(service_signed_in, user_id_before=session_id_current)
      return service_signed_in, screen_signed_in
    else:
      # Assign signed in session id.
      service._session_id = session_id_signed_in
      service._if_signed_in = True
      service._user_name = fase_database.FaseDatabaseInterface.Get().GetUser(user_id=session_id_signed_in).DisplayName()
      screen = on_sign_in_done(service, user_id_before=session_id_current)
      return service, screen


@json_util.JSONDecorator({})
class FaseSignOutButton(fase.Button):

  def FaseOnClick(self, service, screen):
    # Delete screen before.
    screen_before_session_id = service.PopStringVariable(id_='fase_sign_in_screen_before_session_id_str').GetValue()
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)

    service_cls = fase.Service.service_cls
    service = service_cls()
    screen = service.OnStart()
    return service, screen


# TODO(igushev): fase_sign_in variables should be in separated better from services own variables.
def StartSignIn(service, on_sign_in_done=None, skip_option=False, cancel_option=False):
  assert fase_database.FaseDatabaseInterface.Get().GetUser(user_id=service.GetSessionId()) is None
  screen_before = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=service.GetSessionId())
  screen_before_session_id = fase.GenerateSessionId()
  screen_before._session_id = screen_before_session_id
  fase_database.FaseDatabaseInterface.Get().AddScreen(screen_before)
  service.AddFunctionVariable(id_='fase_sign_in_on_sign_in_done_class_method', value=on_sign_in_done)
  service.AddStringVariable(id_='fase_sign_in_screen_before_session_id_str', value=screen_before_session_id)

  screen = fase.Screen(service)
  sign_in_layout = screen.AddLayout(id_='sign_in_layout_id', orientation=fase.Layout.VERTICAL)
  sign_in_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=OnSignInOption)
  sign_in_layout.AddButton(id_='sign_up_button_id', text='Sign Up', on_click=OnSignUpOption)
  if skip_option:
    sign_in_layout.AddButton(id_='skip_button_id', text='Skip', on_click=OnSkipCancelOption)
  elif cancel_option:
    screen.AddPrevStepButton(on_click=OnSkipCancelOption)
  return screen


def OnSignInOption(service, screen, element):
  screen = fase.Screen(service)
  sign_in_layout = screen.AddLayout(id_='sign_in_layout_id', orientation=fase.Layout.VERTICAL)
  sign_in_layout.AddText(id_='phone_number_text_id', hint='Phone Number')
  sign_in_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=OnSignInEnteredData)
  screen.AddPrevStepButton(on_click=StartSignIn)
  return screen


def OnSignInEnteredData(service, screen, element):
  sign_in_layout = screen.GetElement(id_='sign_in_layout_id')
  phone_number = sign_in_layout.GetText(id_='phone_number_text_id').GetText()
  user_list = fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number)
  if not user_list:
    screen.AddPopup('User with such phone number has not been found!')
    return screen
  assert len(user_list) == 1
  user = user_list[0]
  return _OnEnteredData(service, phone_number, user.user_id)


def OnSignUpOption(service, screen, element):
  screen = fase.Screen(service)
  sign_up_layout = screen.AddLayout(id_='sign_up_layout_id', orientation=fase.Layout.VERTICAL)
  sign_up_layout.AddText(id_='phone_number_text_id', hint='Phone Number')
  sign_up_layout.AddText(id_='first_name_text_id', hint='First Name')
  sign_up_layout.AddText(id_='last_name_text_id', hint='Last Name')
  sign_up_layout.AddButton(id_='sign_up_button_id', text='Sign Up', on_click=OnSignUpEnteredData)
  screen.AddPrevStepButton(on_click=StartSignIn)
  return screen
  

def OnSignUpEnteredData(service, screen, element):
  sign_up_layout = screen.GetElement(id_='sign_up_layout_id')
  phone_number = sign_up_layout.GetText(id_='phone_number_text_id').GetText()
  user_list = fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number)
  if user_list:
    screen.AddPopup('User with such phone number is already registered!')
    return screen

  datetime_now = datetime.datetime.now()
  user_id_hash = hashlib.md5()
  user_id_hash.update(datetime_now.strftime(fase.DATETIME_FORMAT_HASH).encode('utf-8'))
  user_id_hash.update(phone_number.encode('utf-8'))
  user_id = user_id_hash.hexdigest()
  
  user = fase_model.User(user_id=user_id,
                         phone_number=sign_up_layout.GetText(id_='phone_number_text_id').GetText(),
                         first_name=sign_up_layout.GetText(id_='first_name_text_id').GetText(),
                         last_name=sign_up_layout.GetText(id_='last_name_text_id').GetText(),
                         datetime_added=datetime_now)
  fase_database.FaseDatabaseInterface.Get().AddUser(user)
  return _OnEnteredData(service, phone_number, user_id)


def _OnEnteredData(service, phone_number, user_id):
  activation_code = activation_code_generator.ActivationCodeGenerator.Get().Generate()
  sms_sender.SMSSender.Get().SendActivationCode(phone_number, activation_code)
  screen = fase.Screen(service)
  enter_activation_layout = screen.AddLayout(id_='enter_activation_layout_id', orientation=fase.Layout.VERTICAL)
  enter_activation_layout.AddText(id_='activation_code_text_id', hint='Activation Code')
  enter_activation_layout.AddElement(id_='send_button_id', element=FaseSignInButton(text='Send'))
  service.AddStringVariable(id_='fase_sign_in_session_id_signed_in_str', value=user_id)
  service.AddIntVariable(id_='fase_sign_in_activation_code_int', value=activation_code)
  screen.AddPrevStepButton(on_click=StartSignIn)
  return screen


def StartSignOut(service, cancel_option=False):
  assert fase_database.FaseDatabaseInterface.Get().GetUser(user_id=service.GetSessionId()) is not None
  screen_before = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=service.GetSessionId())
  screen_before_session_id = fase.GenerateSessionId()
  screen_before._session_id = screen_before_session_id
  fase_database.FaseDatabaseInterface.Get().AddScreen(screen_before)
  service.AddStringVariable(id_='fase_sign_in_screen_before_session_id_str', value=screen_before_session_id)

  screen = fase.Screen(service)
  sign_out_layout = screen.AddLayout(id_='sign_out_layout_id', orientation=fase.Layout.VERTICAL)
  sign_out_layout.AddElement(id_='sign_out_button_id', element=FaseSignOutButton(text='Sign Out'))
  if cancel_option:
    screen.AddPrevStepButton(on_click=OnSkipCancelOption)
  return screen


def OnSkipCancelOption(service, screen, element):
  service.PopStringVariable(id_='fase_sign_in_on_sign_in_done_class_method')
  screen_before_session_id = service.PopStringVariable(id_='fase_sign_in_screen_before_session_id_str').GetValue() 
  screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_id=screen_before_session_id)
  screen._session_id = service.GetSessionId()
  fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)
  # Delete same object by old key.
  fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=screen_before_session_id)
  return screen
