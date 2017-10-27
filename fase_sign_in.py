import datetime
import functools
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
    session_id = service.GetStringVariable(id_='fase_sign_in_session_id_str').GetValue()
    service_signed_in = fase_database.FaseDatabaseInterface.Get().GetService(session_id=session_id)
    screen_signed_in = on_sign_in_done(service_signed_in, cancelled=False, skipped=False, user_id_before=service._session_id)
    session_id_before = service._session_id
    fase_database.FaseDatabaseInterface.Get().DeleteService(session_id=session_id_before)
    fase_database.FaseDatabaseInterface.Get().DeleteScreen(session_id=session_id_before)
    return service_signed_in, screen_signed_in 


# TODO(igushev): fase_sign_in variables should be in separated better from services own variables.
class FaseSignIn(object):

  @staticmethod
  def Start(service, on_sign_in_done=None, cancel_option=False, skip_option=False):
    service.AddClassMethodVariable('fase_sign_in_on_sign_in_done_class_method', on_sign_in_done)
    service.AddBoolVariable('fase_sign_in_cancel_option_bool', cancel_option)
    screen = fase.Screen()
    sign_in_layout = screen.AddLayout(id_='sign_in_layout_id', orientation=fase.Layout.VERTICAL)
    sign_in_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=FaseSignIn.OnSignInOption)
    sign_in_layout.AddButton(id_='sign_up_button_id', text='Sign Up', on_click=FaseSignIn.OnSignUpOption)
    if skip_option:
      sign_in_layout.AddButton(id_='skip_button_id', text='Skip', on_click=FaseSignIn.OnSkipOption)
    if service.GetBoolVariable('fase_sign_in_cancel_option_bool').GetValue():
      screen.AddPrevStepButton(on_click=FaseSignIn.OnCancelOption)
    return screen

  @staticmethod
  def OnSignInOption(service, screen, element):
    screen = fase.Screen()
    sign_in_layout = screen.AddLayout(id_='sign_in_layout_id', orientation=fase.Layout.VERTICAL)
    sign_in_layout.AddText(id_='phone_number_text_id', hint='Phone Number')
    sign_in_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=FaseSignIn.OnSignInEnteredData)
    if service.GetBoolVariable('fase_sign_in_cancel_option_bool').GetValue():
      screen.AddPrevStepButton(on_click=FaseSignIn.OnCancelOption)
    return screen

  @staticmethod
  def OnSignInEnteredData(service, screen, element):
    sign_in_layout = screen.GetElement(id_='sign_in_layout_id')
    phone_number = sign_in_layout.GetText(id_='phone_number_text_id').GetText()
    user = fase_database.FaseDatabaseInterface.Get().GetUserByPhoneNumber(phone_number)
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
    sign_up_layout.AddButton(id_='sign_in_button_id', text='Sign In', on_click=FaseSignIn.OnSignUpEnteredData)
    if service.GetBoolVariable('fase_sign_in_cancel_option_bool').GetValue():
      screen.AddPrevStepButton(on_click=FaseSignIn.OnCancelOption)
    return screen
    
  @staticmethod
  def OnSignUpEnteredData(service, screen, element):
    sign_up_layout = screen.GetElement('sign_up_layout_id')
    phone_number = sign_up_layout.GetText(id_='phone_number_text_id')
    if fase_database.FaseDatabaseInterface.Get().GetUserByPhoneNumber(phone_number):
      return fase.Popup('User with such phone number is already registered!')

    datetime_now = datetime.datetime.now()
    user_id_hash = hashlib.md5()
    user_id_hash.update(datetime_now.strftime(fase.DATETIME_FORMAT_HASH))
    user_id_hash.update(phone_number)
    user_id = user_id_hash.hexdigest()
    
    user = fase_model.User(user_id=user_id,
                           phone_number=sign_up_layout.GetText(id_='phone_number').GetText(),
                           first_name=sign_up_layout.GetText(id_='first_name').GetText(),
                           last_name=sign_up_layout.GetText(id_='last_name').GetText(),
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
    service.AddStringVariable(id_='fase_sign_in_session_id_str', value=user_id)
    service.AddIntVariable(id_='fase_sign_in_activation_code_str', value=activation_code)
    screen.AddPrevStepButton(on_click=FaseSignIn.Start)
    return screen

  @staticmethod
  def OnSkipOption(service):
    on_sign_in_done = service.GetClassMethodVariable('fase_sign_in_on_sign_in_done_class_method')
    return on_sign_in_done(service, cancelled=False, skipped=True, service_before=None, screen_before=None)

  @staticmethod
  def OnCancelOption(service, screen, element):
    on_sign_in_done = service.GetClassMethodVariable('fase_sign_in_on_sign_in_done_class_method')
    return on_sign_in_done(service, cancelled=True, skipped=False, service_before=None, screen_before=None)
