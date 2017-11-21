import activation_code_generator
import fase_model
import fase_server
import sms_sender


def SignInProcedure(session_info, screen_info, sign_in_id_list,
                    sign_in=None, phone_number=None, first_name=None, last_name=None):
  assert sign_in is not None
  activation_code_generator.ActivationCodeGeneratorInterface.Set(
      activation_code_generator.MockActivationCodeGenerator(activation_code_generator.ActivationCodeGenerator()),
      overwrite=True)
  sms_sender.SMSSender.Set(sms_sender.SMSSender(sms_sender.MockSMSServiceProvider()), overwrite=True)

  # Click on Sign In button.
  response = fase_server.FaseServer.Get().ElementClicked(fase_model.ElementClicked(sign_in_id_list), session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  screen = response.screen
  # Check present of main elements.
  screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_in_button_id')
  screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_up_button_id')

  if sign_in:
    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(fase_model.ElementClicked(['sign_in_layout_id', 'sign_in_button_id']),
                                           session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='sign_in_layout_id').GetElement(id_='phone_number_text_id')
    screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_in_button_id')

    # Enter phone number.
    screen_update = fase_model.ScreenUpdate([['sign_in_layout_id', 'phone_number_text_id']], [phone_number])
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(['sign_in_layout_id', 'sign_in_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
  else:
    # Click on Sign Up button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(['sign_in_layout_id', 'sign_up_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check present of main elements.
    screen.GetElement(id_='sign_up_layout_id').GetElement(id_='phone_number_text_id')
    screen.GetElement(id_='sign_up_layout_id').GetElement(id_='first_name_text_id')
    screen.GetElement(id_='sign_up_layout_id').GetElement(id_='last_name_text_id')
    screen.GetElement(id_='sign_up_layout_id').GetElement(id_='sign_up_button_id')

    # Enter phone number.
    screen_update = fase_model.ScreenUpdate([['sign_up_layout_id', 'phone_number_text_id'],
                                             ['sign_up_layout_id', 'first_name_text_id'],
                                             ['sign_up_layout_id', 'last_name_text_id']], [phone_number,
                                                                                           first_name,
                                                                                           last_name])
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign Up button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(['sign_up_layout_id', 'sign_up_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
  
  # Check present of main elements.
  screen.GetElement(id_='enter_activation_layout_id').GetElement(id_='activation_code_text_id')
  screen.GetElement(id_='enter_activation_layout_id').GetElement(id_='send_button_id')

  # Enter activation code.
  screen_update = fase_model.ScreenUpdate(
      [['enter_activation_layout_id', 'activation_code_text_id']],
      [str(activation_code_generator.ActivationCodeGeneratorInterface.Get().codes[-1])])
  fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
  # Click on Send button.
  response = fase_server.FaseServer.Get().ElementClicked(
      fase_model.ElementClicked(['enter_activation_layout_id', 'send_button_id']), session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  screen = response.screen
  return session_info, screen_info, screen


def SignOutProcedure(session_info, screen_info, sign_out_id_list):
  # Click on Sign Out button.
  response = fase_server.FaseServer.Get().ElementClicked(
      fase_model.ElementClicked(sign_out_id_list), session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  screen = response.screen
  # Check present of main elements.
  screen.GetElement(id_='sign_out_layout_id').GetElement(id_='sign_out_button_id')

  # Click on Sign Out button.
  response = fase_server.FaseServer.Get().ElementClicked(
      fase_model.ElementClicked(['sign_out_layout_id', 'sign_out_button_id']), session_info, screen_info)
  session_info = response.session_info
  screen_info = response.screen_info
  return session_info, screen_info
