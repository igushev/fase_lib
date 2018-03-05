from server_util import activation_code_generator
from server_util import sms_sender

from fase import fase
from fase_model import fase_model

try:
  from . import fase_sign_in_impl
  from . import fase_server
except SystemError:  
  import fase_sign_in_impl
  import fase_server

COUNTRY_CODE = 'US'


def SignInProcedure(session_info, screen_info, sign_in_id_list,
                    sign_in=None, phone_number=None, first_name=None, last_name=None):
  assert sign_in is not None
  activation_code_generator.ActivationCodeGeneratorInterface.Set(
      activation_code_generator.MockActivationCodeGenerator(activation_code_generator.ActivationCodeGenerator()),
      overwrite=True)
  sms_sender.SMSSender.Set(sms_sender.SMSSender(sms_sender.MockSMSServiceProvider()), overwrite=True)

  # Click on Sign In button.
  response = fase_server.FaseServer.Get().ElementCallback(
      fase_model.ElementCallback(id_list=sign_in_id_list, method=fase.ON_CLICK_METHOD), session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  screen = response.screen
  # Check present of main elements.
  screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_in_button_id')
  screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_up_button_id')

  if sign_in:
    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=['sign_in_frame_id', 'sign_in_button_id'], method=fase.ON_CLICK_METHOD),
        session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='sign_in_frame_id').GetElement(id_='phone_number_text_id')
    screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_in_button_id')

    # Enter phone number.
    elements_update=fase_model.ElementsUpdate([['sign_in_frame_id', 'phone_number_text_id']], [phone_number])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=['sign_in_frame_id', 'sign_in_button_id'], method=fase.ON_CLICK_METHOD,
                                   locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
  else:
    # Click on Sign Up button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=['sign_in_frame_id', 'sign_up_button_id'], method=fase.ON_CLICK_METHOD),
        session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='sign_up_frame_id').GetElement(id_='phone_number_text_id')
    screen.GetElement(id_='sign_up_frame_id').GetElement(id_='first_name_text_id')
    screen.GetElement(id_='sign_up_frame_id').GetElement(id_='last_name_text_id')
    screen.GetElement(id_='sign_up_frame_id').GetElement(id_='sign_up_button_id')

    # Enter phone number.
    elements_update=fase_model.ElementsUpdate([['sign_up_frame_id', 'phone_number_text_id'],
                                               ['sign_up_frame_id', 'first_name_text_id'],
                                               ['sign_up_frame_id', 'last_name_text_id']], [phone_number,
                                                                                             first_name,
                                                                                             last_name])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign Up button.
    response = fase_server.FaseServer.Get().ElementCallback(
        fase_model.ElementCallback(id_list=['sign_up_frame_id', 'sign_up_button_id'], method=fase.ON_CLICK_METHOD,
                                   locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
  
  # Check present of main elements.
  screen.GetElement(id_='enter_activation_frame_id').GetElement(id_='activation_code_text_id')
  screen.GetElement(id_='enter_activation_frame_id').GetElement(id_='send_button_id')

  # Enter activation code.
  elements_update=fase_model.ElementsUpdate(
      [['enter_activation_frame_id', 'activation_code_text_id']],
      [str(activation_code_generator.ActivationCodeGeneratorInterface.Get().codes[-1])])
  screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
  fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
  # Click on Send button.
  response = fase_server.FaseServer.Get().ElementCallback(
      fase_model.ElementCallback(id_list=['enter_activation_frame_id', 'send_button_id'], method=fase.ON_CLICK_METHOD),
      session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  screen = response.screen
  return session_info, screen_info, screen


def SignOutProcedure(session_info, screen_info, sign_out_id_list):
  # Click on Sign Out button.
  response = fase_server.FaseServer.Get().ElementCallback(
      fase_model.ElementCallback(id_list=sign_out_id_list, method=fase.ON_CLICK_METHOD), session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  screen = response.screen
  # Check present of main elements.
  screen.GetElement(id_='sign_out_frame_id').GetElement(id_='sign_out_button_id')

  # Click on Sign Out button.
  response = fase_server.FaseServer.Get().ElementCallback(
      fase_model.ElementCallback(id_list=['sign_out_frame_id', 'sign_out_button_id'], method=fase.ON_CLICK_METHOD),
      session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  return session_info, screen_info
