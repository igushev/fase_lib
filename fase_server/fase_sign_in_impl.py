import datetime
import hashlib
import sys

from fase_lib import fase
from fase_lib import fase_sign_in
from fase_lib.base_util import json_util
from fase_lib.server_util import activation_code_generator
from fase_lib.server_util import phone_number_verifier
from fase_lib.server_util import sms_sender
from fase_lib.fase_model import fase_model

try:
  from fase_lib.fase_server import fase_database
  from fase_lib.fase_server import fase_demo_data
except ImportError:
  import fase_database
  import fase_demo_data

ACTIVATION_CODE_MSG = 'Your activation code is %d.'


# Register itself as API implementation.
fase_sign_in.fase_sign_in_impl = sys.modules[__name__]


def GenerateSignedInSessionId(user_id):
  service_cls = fase.Service.service_cls
  session_id_signed_in_hash = hashlib.md5()
  session_id_signed_in_hash.update(service_cls.GetServiceId().encode('utf-8'))
  session_id_signed_in_hash.update(user_id.encode('utf-8'))
  session_id_signed_in = session_id_signed_in_hash.hexdigest()
  return session_id_signed_in


USER_NOT_FOUND = 'User with such phone number has not been found!'
USER_ALREADY_REGISTERED = 'User with such phone number is already registered!'
PHONE_NOT_SPECIFIED = 'Phone number is not specified!'
PHONE_IS_INVALID = 'Phone number format is invalid!'
PHONE_NO_COUNTRY_CODE = 'Phone number country code could not be inferred! Please try to add explicitly!'
NO_DATE_OF_BIRTH = 'Please enter Date of Birth!'
NO_PLACE = 'Please enter Home City!'
GOOGLE_PLACE_ID_IS_NOT_SPECIFIED = (
  'Google Place Id is not specified! Try to update Google Services, restart the application or reboot the phone!')
NO_ACTIVATION_CODE = 'No activation code!'
WRONG_ACTIVATION_CODE = 'Wrong activation code!'
UNDER_AGE_USER = 'To Sign Up You must be at least %s years old!'


def _ErrorAlert(service, message, on_click):
  screen = fase.Screen(service)
  alert = screen.AddAlert(message)
  alert.AddButton(id_="ok_id", text="OK", on_click=on_click)
  return screen


@json_util.JSONDecorator({})
class FaseSignInButton(fase.Button):

  def CallCallback(self, service_prog, screen_prog, device, method):
    assert method == fase.ON_CLICK_METHOD
    service = service_prog.service
    activation_code_sent = service.PopIntVariable(id_='fase_sign_in_activation_code_int').GetValue()
    activation_code_text = (
        screen_prog.screen.GetFrame(id_='enter_activation_frame_id').GetText(id_='activation_code_text_id').GetText())
    if not activation_code_text:
      service.AddIntVariable(id_='fase_sign_in_activation_code_int', value=activation_code_sent)
      screen_prog.screen = _ErrorAlert(service, message=NO_ACTIVATION_CODE, on_click=OnActivationCodeSent)
      return service_prog, screen_prog
    activation_code_entered = int(activation_code_text)
    if activation_code_sent != activation_code_entered:
      service.AddIntVariable(id_='fase_sign_in_activation_code_int', value=activation_code_sent)
      screen_prog.screen = _ErrorAlert(service, message=WRONG_ACTIVATION_CODE, on_click=OnActivationCodeSent)
      return service_prog, screen_prog 

    on_done = service.PopFunctionVariable(id_='fase_sign_in_on_done_class_method').GetValue()
    if service.HasFunctionVariable(id_='fase_sign_in_on_skip_class_method'):
      service.PopFunctionVariable(id_='fase_sign_in_on_skip_class_method')
    if service.HasFunctionVariable(id_='fase_sign_in_on_cancel_class_method'):
      service.PopFunctionVariable(id_='fase_sign_in_on_cancel_class_method')
    service.PopStringVariable(id_='fase_sign_in_request_user_data')
    user_id = service.PopStringVariable(id_='fase_sign_in_user_id_str').GetValue()
    # NOTE(igushev): We should either lookup by user_id and service_id and have deterministic hash.
    session_id_signed_in = GenerateSignedInSessionId(user_id)
    # Delete service and screen current.
    user_id_before = service.GetUserId()
    session_id_current = service_prog.session_id
    fase_database.FaseDatabaseInterface.Get().DeleteServiceProg(session_id=session_id_current)
    fase_database.FaseDatabaseInterface.Get().DeleteScreenProg(session_id=session_id_current)

    try:
      service_prog_signed_in = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id=session_id_signed_in)
    except Exception:
      service_prog_signed_in = None

    if service_prog_signed_in:
      # Retrieve sign in service and call.
      screen_prog_signed_in = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_id=session_id_signed_in)
      service_prog_signed_in.device_list.append(device)
      screen_prog_signed_in.screen = on_done(service_prog_signed_in.service, user_id_before=user_id_before)
      return service_prog_signed_in, screen_prog_signed_in
    else:
      # Assign signed in session id.
      user = fase_database.FaseDatabaseInterface.Get().GetUser(user_id=user_id)
      service_prog.session_id = session_id_signed_in
      service._session_id = session_id_signed_in
      service._if_signed_in = True
      service._user_id = user_id
      service._user = user
      screen_prog.screen = on_done(service, user_id_before=user_id_before)
      screen_prog.session_id = session_id_signed_in
      return service_prog, screen_prog


@json_util.JSONDecorator({})
class FaseSignOutButton(fase.Button):

  def CallCallback(self, service_prog, screen_prog, device, method):
    assert method == fase.ON_CLICK_METHOD
    for i, device_signed_in in enumerate(service_prog.device_list):
      if fase_model.SameDevice(device_signed_in, device):
        del service_prog.device_list[i]
        break
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog, overwrite=True)
    return fase_model.GetServiceProgScreenProg(device)


def StartSignIn(service, on_done=None, on_skip=None, on_cancel=None, request_user_data=None):
  assert not service.IfSignedIn()
  service.AddFunctionVariable(id_='fase_sign_in_on_done_class_method', value=on_done)
  if on_skip is not None:
    service.AddFunctionVariable(id_='fase_sign_in_on_skip_class_method', value=on_skip)
  if on_cancel is not None:
    service.AddFunctionVariable(id_='fase_sign_in_on_cancel_class_method', value=on_cancel)
  
  # Requested user data.
  request_user_data = request_user_data or fase.RequestUserData()
  service.AddStringVariable(id_='fase_sign_in_request_user_data', value=request_user_data.ToJSON())
  return OnSignInStart(service, None, None)


def OnSignInStart(service, screen, element):
  screen = fase.Screen(service)
  screen.SetTitle('Sign In')
  sign_in_frame = screen.AddFrame(id_='sign_in_frame_id', orientation=fase.Frame.VERTICAL)
  sign_in_frame.AddButton(id_='sign_in_button_id', text='Sign In', on_click=OnSignInOption)
  sign_in_frame.AddButton(id_='sign_up_button_id', text='Sign Up', on_click=OnSignUpOption)
  if service.HasFunctionVariable(id_='fase_sign_in_on_skip_class_method'):
    sign_in_frame.AddButton(id_='skip_button_id', text='Skip', on_click=OnSignInSkipOption)
  if service.HasFunctionVariable(id_='fase_sign_in_on_cancel_class_method'):
    screen.AddPrevStepButton(text='Cancel', on_click=OnSignInCancelOption)
  return screen


def OnSignInOption(service, screen, element):
  screen = fase.Screen(service)
  screen.SetTitle('Sign In')
  sign_in_frame = screen.AddFrame(id_='sign_in_frame_id', orientation=fase.Frame.VERTICAL)
  sign_in_frame.AddText(id_='phone_number_text_id', hint='Phone Number', type_=fase.Text.PHONE)
  sign_in_button = sign_in_frame.AddButton(id_='sign_in_button_id', text='Sign In', on_click=OnSignInEnteredData)
  sign_in_button.SetRequestLocale(True)
  screen.AddPrevStepButton(text='Back', on_click=OnSignInStart)
  return screen


def OnSignInEnteredData(service, screen, element):
  sign_in_frame = screen.GetElement(id_='sign_in_frame_id')
  phone_number = sign_in_frame.GetText(id_='phone_number_text_id').GetText()
  country_code = element.GetLocale().country_code

  if country_code:
    country_code = country_code.upper()

  if not phone_number:
    return _ErrorAlert(service, message=PHONE_NOT_SPECIFIED, on_click=OnSignInOption)
  try:
    phone_number = phone_number_verifier.Format(phone_number, country_code)
  except phone_number_verifier.NoCountryCodeException:
    return _ErrorAlert(service, message=PHONE_NO_COUNTRY_CODE, on_click=OnSignInOption)
  except phone_number_verifier.InvalidPhoneNumberException:
    return _ErrorAlert(service, message=PHONE_IS_INVALID, on_click=OnSignInOption)

  user_list = fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number)
  if not user_list:
    return _ErrorAlert(service, message=USER_NOT_FOUND, on_click=OnSignInOption)
  assert len(user_list) == 1
  user = user_list[0]
  _CleanUserVariables(service)
  service.AddStringVariable(id_='fase_sign_in_user_id_str', value=user.user_id)

  # Requested user data.
  request_user_data = fase.RequestUserData.FromJSON(
      service.GetStringVariable(id_='fase_sign_in_request_user_data').GetValue())
  if ((request_user_data.date_of_birth and user.date_of_birth is None) or
      (request_user_data.home_city and user.home_city is None)):
    return _OnRequestUserData(service, screen, element, request_user_data, user)
  
  return _OnEnteredData(service, screen, element, phone_number)


def _OnRequestUserData(service, screen, element, request_user_data, user):
  screen = fase.Screen(service)
  screen.SetTitle('Enter Data')
  enter_frame = screen.AddFrame(id_='enter_frame_id', orientation=fase.Frame.VERTICAL)

  if request_user_data.date_of_birth and user.date_of_birth is None:
    enter_frame.AddDateTimePicker(id_='date_of_birth_date_picker', type_=fase.DateTimePicker.DATE,
                                   hint='Date of Birth')
  if request_user_data.home_city and user.home_city is None:
    enter_frame.AddPlacePicker(id_='home_city_place_picker', type_=fase.PlacePicker.CITY, hint='Home City')

  enter_button = enter_frame.AddButton(id_='enter_button_id', text='Enter', on_click=OnRequestUserDataEnteredData)
  enter_button.SetRequestLocale(True)
  screen.AddPrevStepButton(text='Back', on_click=OnSignInStart)
  return screen


def OnRequestUserDataEnteredData(service, screen, element):
  user_id = service.GetStringVariable(id_='fase_sign_in_user_id_str').GetValue()
  user = fase_database.FaseDatabaseInterface.Get().GetUser(user_id=user_id)

  # Requested user data.
  request_user_data = fase.RequestUserData.FromJSON(
      service.GetStringVariable(id_='fase_sign_in_request_user_data').GetValue())
  enter_frame = screen.GetElement(id_='enter_frame_id')

  if request_user_data.date_of_birth and user.date_of_birth is None:
    date_of_birth = enter_frame.GetDateTimePicker(id_='date_of_birth_date_picker').GetDateTime()
    if date_of_birth is None:
      return _ErrorAlert(service, message=NO_DATE_OF_BIRTH, on_click=OnSignUpOption)
    if request_user_data.min_date_of_birth is not None and request_user_data.min_date_of_birth < date_of_birth:
      min_age = datetime.datetime.utcnow() - request_user_data.min_date_of_birth
      return _ErrorAlert(service, message=UNDER_AGE_USER % (min_age.days // 365), on_click=OnSignUpOption)
    user.date_of_birth = date_of_birth
  if request_user_data.home_city and user.home_city is None:
    home_city = enter_frame.GetPlacePicker(id_='home_city_place_picker').GetPlace()
    if home_city is None:
      return _ErrorAlert(service, message=NO_PLACE, on_click=OnSignUpOption)
    if not home_city.google_place_id:
      return _ErrorAlert(service, message=GOOGLE_PLACE_ID_IS_NOT_SPECIFIED, on_click=OnSignUpOption)
    user.home_city = home_city

  fase_database.FaseDatabaseInterface.Get().AddUser(user, overwrite=True)
  return _OnEnteredData(service, screen, element, user.GetPhoneNumber())


def OnSignUpOption(service, screen, element):
  screen = fase.Screen(service)
  screen.SetTitle('Sign Up')
  sign_up_frame = screen.AddFrame(id_='sign_up_frame_id', orientation=fase.Frame.VERTICAL)
  sign_up_frame.AddText(id_='phone_number_text_id', hint='Phone Number', type_=fase.Text.PHONE)
  sign_up_frame.AddText(id_='first_name_text_id', hint='First Name')
  sign_up_frame.AddText(id_='last_name_text_id', hint='Last Name')

  # Requested user data.
  request_user_data = fase.RequestUserData.FromJSON(
      service.GetStringVariable(id_='fase_sign_in_request_user_data').GetValue())

  if request_user_data.date_of_birth:
    sign_up_frame.AddDateTimePicker(id_='date_of_birth_date_picker', type_=fase.DateTimePicker.DATE,
                                     hint='Date of Birth')
  if request_user_data.home_city:
    sign_up_frame.AddPlacePicker(id_='home_city_place_picker', type_=fase.PlacePicker.CITY, hint='Home City')

  sign_up_button = sign_up_frame.AddButton(id_='sign_up_button_id', text='Sign Up', on_click=OnSignUpEnteredData)
  sign_up_button.SetRequestLocale(True)
  screen.AddPrevStepButton(text='Back', on_click=OnSignInStart)
  return screen
  

def OnSignUpEnteredData(service, screen, element):
  sign_up_frame = screen.GetElement(id_='sign_up_frame_id')
  phone_number = sign_up_frame.GetText(id_='phone_number_text_id').GetText()
  locale = element.GetLocale()
  country_code = locale.GetCountryCode()

  if country_code:
    country_code = country_code.upper()

  if not phone_number:
    return _ErrorAlert(service, message=PHONE_NOT_SPECIFIED, on_click=OnSignUpOption)
  try:
    phone_number = phone_number_verifier.Format(phone_number, country_code)
  except phone_number_verifier.NoCountryCodeException:
    return _ErrorAlert(service, message=PHONE_NO_COUNTRY_CODE, on_click=OnSignUpOption)
  except phone_number_verifier.InvalidPhoneNumberException:
    return _ErrorAlert(service, message=PHONE_IS_INVALID, on_click=OnSignUpOption)
  
  user_list = fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number)
  if user_list:
    return _ErrorAlert(service, message=USER_ALREADY_REGISTERED, on_click=OnSignUpOption)

  datetime_now = datetime.datetime.utcnow()
  user_id_hash = hashlib.md5()
  user_id_hash.update(datetime_now.strftime(fase.DATETIME_FORMAT_HASH).encode('utf-8'))
  user_id_hash.update(phone_number.encode('utf-8'))
  user_id = user_id_hash.hexdigest()

  first_name = sign_up_frame.GetText(id_='first_name_text_id').GetText()
  last_name = sign_up_frame.GetText(id_='last_name_text_id').GetText()

  # Requested user data.
  request_user_data = fase.RequestUserData.FromJSON(
      service.GetStringVariable(id_='fase_sign_in_request_user_data').GetValue())

  if request_user_data.date_of_birth:
    date_of_birth = sign_up_frame.GetDateTimePicker(id_='date_of_birth_date_picker').GetDateTime()
    if date_of_birth is None:
      return _ErrorAlert(service, message=NO_DATE_OF_BIRTH, on_click=OnSignUpOption)
    if request_user_data.min_date_of_birth is not None and request_user_data.min_date_of_birth < date_of_birth:
      min_age = datetime.datetime.utcnow() - request_user_data.min_date_of_birth
      return _ErrorAlert(service, message=UNDER_AGE_USER % (min_age.days // 365), on_click=OnSignUpOption)
  else:
    date_of_birth = None
  if request_user_data.home_city:
    home_city = sign_up_frame.GetPlacePicker(id_='home_city_place_picker').GetPlace()
    if home_city is None:
      return _ErrorAlert(service, message=NO_PLACE, on_click=OnSignUpOption)
    if not home_city.google_place_id:
      return _ErrorAlert(service, message=GOOGLE_PLACE_ID_IS_NOT_SPECIFIED, on_click=OnSignUpOption)
  else:
    home_city = None

  user = fase.User(user_id=user_id,
                   phone_number=phone_number,
                   first_name=first_name,
                   last_name=last_name,
                   date_of_birth=date_of_birth,
                   home_city=home_city,
                   locale=locale,
                   datetime_added=datetime_now)
  fase_database.FaseDatabaseInterface.Get().AddUser(user)
  _CleanUserVariables(service)
  service.AddStringVariable(id_='fase_sign_in_user_id_str', value=user_id)
  return _OnEnteredData(service, screen, element, phone_number)


def _OnEnteredData(service, screen, element, phone_number):
  if fase_demo_data.PhoneNumberIsDemo(phone_number):
    activation_code = fase_demo_data.DEMO_ACTIVATION_CODE
  else:
    activation_code = activation_code_generator.ActivationCodeGenerator.Get().Generate()
    sms_sender.SMSSender.Get().Send(phone_number, ACTIVATION_CODE_MSG % activation_code)
  _CleanActivationVariables(service)
  service.AddIntVariable(id_='fase_sign_in_activation_code_int', value=activation_code)
  return OnActivationCodeSent(service, screen, element)


def OnActivationCodeSent(service, screen, element):
  screen = fase.Screen(service)
  screen.SetTitle('Activation Code')
  enter_activation_frame = screen.AddFrame(id_='enter_activation_frame_id', orientation=fase.Frame.VERTICAL)
  enter_activation_frame.AddText(id_='activation_code_text_id', hint='Activation Code', type_=fase.Text.DIGITS)
  enter_activation_frame.AddElement(
      id_='send_button_id', element=FaseSignInButton(text='Send', on_click=fase.FunctionPlaceholder))
  screen.AddPrevStepButton(text='Back', on_click=OnSignInStart)
  return screen


def OnSignInSkipOption(service, screen, element):
  service.PopFunctionVariable(id_='fase_sign_in_on_done_class_method')
  on_skip = service.PopFunctionVariable(id_='fase_sign_in_on_skip_class_method').GetValue()
  if service.HasFunctionVariable(id_='fase_sign_in_on_cancel_class_method'):
    service.PopFunctionVariable(id_='fase_sign_in_on_cancel_class_method')
  service.PopStringVariable(id_='fase_sign_in_request_user_data')
  _CleanUserVariables(service)
  _CleanActivationVariables(service)
  screen = on_skip(service)
  return screen


def OnSignInCancelOption(service, screen, element):
  service.PopFunctionVariable(id_='fase_sign_in_on_done_class_method')
  if service.HasFunctionVariable(id_='fase_sign_in_on_skip_class_method'):
    service.PopFunctionVariable(id_='fase_sign_in_on_skip_class_method')
  on_cancel = service.PopFunctionVariable(id_='fase_sign_in_on_cancel_class_method').GetValue()
  service.PopStringVariable(id_='fase_sign_in_request_user_data')
  _CleanUserVariables(service)
  _CleanActivationVariables(service)
  screen = on_cancel(service)
  return screen


def _CleanUserVariables(service):
  if service.HasStringVariable(id_='fase_sign_in_user_id_str'):
    service.PopStringVariable(id_='fase_sign_in_user_id_str')


def _CleanActivationVariables(service):
  if service.HasIntVariable(id_='fase_sign_in_activation_code_int'):
    service.PopIntVariable(id_='fase_sign_in_activation_code_int')


def StartSignOut(service, on_cancel=None):
  assert service.IfSignedIn()

  screen = fase.Screen(service)
  screen.SetTitle('Sign Out')
  screen.AddLabel(id_='user_name_label_id', text=service.GetUser().DisplayName())
  sign_out_frame = screen.AddFrame(id_='sign_out_frame_id', orientation=fase.Frame.VERTICAL)
  sign_out_frame.AddElement(
      id_='sign_out_button_id', element=FaseSignOutButton(text='Sign Out', on_click=fase.FunctionPlaceholder))
  if service.HasFunctionVariable(id_='fase_sign_out_on_cancel_class_method'):
    service.PopFunctionVariable(id_='fase_sign_out_on_cancel_class_method')
  if on_cancel is not None:
    service.AddFunctionVariable(id_='fase_sign_out_on_cancel_class_method', value=on_cancel)
    screen.AddPrevStepButton(text='Cancel', on_click=OnSignOutCancelOption)
  return screen


def OnSignOutCancelOption(service, screen, element):
  on_cancel = service.PopFunctionVariable(id_='fase_sign_out_on_cancel_class_method').GetValue()
  screen = on_cancel(service)
  return screen


def GetUserIdByPhoneNumber(phone_number):
  user_list = fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(phone_number)
  if not user_list:
    return None
  assert len(user_list) == 1
  user = next(iter(user_list))
  return user.user_id
