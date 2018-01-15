import datetime
import unittest

import activation_code_generator
import fase_database
import fase_model
import fase_server
import fase_sign_in
import fase
import sms_sender


class SignInTestService(fase.Service):
  
  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddButton(id_='sign_in_button_id',
                     text='Sign In', on_click=SignInTestService.OnSignIn)
    screen.AddButton(id_='sign_out_button_id',
                     text='Sign Out', on_click=SignInTestService.OnSignOut)
    screen.AddButton(id_='about_button_id',
                     text='Abount', on_click=SignInTestService.OnAbount)
    return screen

  def OnSignIn(self, screen, element):
    return fase_sign_in.StartSignIn(
        self, on_sign_in_done=SignInTestService.OnSignInDone, skip_option=True, cancel_option=True)

  def OnSignOut(self, screen, element):
    return fase_sign_in.StartSignOut(self)

  def OnSignInDone(self, user_id_before=None):
    screen = fase.Screen(self)
    screen.AddLabel(id_='user_id_before_label_id', label=user_id_before)
    return screen

  def OnAbount(self, screen, element):
    screen = fase.Screen(self)
    screen.AddLabel(id_='about_label_id', label='Sign In Test Service')
    return screen

fase.Service.RegisterService(SignInTestService)


class FaseSignInTest(unittest.TestCase):

  def setUp(self):
    super(FaseSignInTest, self).setUp()
    activation_code_generator.ActivationCodeGeneratorInterface.Set(
        activation_code_generator.MockActivationCodeGenerator(activation_code_generator.ActivationCodeGenerator()),
        overwrite=True)
    sms_sender.SMSSender.Set(sms_sender.SMSSender(sms_sender.MockSMSServiceProvider()), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def SignInProcedure(self,
                      service_num_before, screen_num_before,
                      service_num_during, screen_num_during,
                      sign_in=None,
                      phone_number=None, first_name=None, last_name=None,
                      expected_user_id=None,
                      return_phone_enter=False,
                      return_activation_code_enter=False):
    assert sign_in is not None
    # Create Service.
    response = fase_server.FaseServer.Get().GetService(fase_model.Device(device_type='iOS', device_token='Token'))
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(service_num_before, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(screen_num_before, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='sign_in_button_id')

    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_in_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_in_button_id')
    screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_up_button_id')

    if sign_in:
      # Click on Sign In button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_layout_id', 'sign_in_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
      # Check.
      self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
      # Check present of main elements.
      screen.GetElement(id_='sign_in_layout_id').GetElement(id_='phone_number_text_id')
      screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_in_button_id')
  
      if return_phone_enter:
        return session_info, screen_info
  
      # Enter phone number.
      screen_update = fase_model.ScreenUpdate([['sign_in_layout_id', 'phone_number_text_id']], [phone_number])
      fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
      # Click on Sign In button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_layout_id', 'sign_in_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
    else:
      # Click on Sign Up button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_layout_id', 'sign_up_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
      # Check.
      self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
      # Check present of main elements.
      screen.GetElement(id_='sign_up_layout_id').GetElement(id_='phone_number_text_id')
      screen.GetElement(id_='sign_up_layout_id').GetElement(id_='first_name_text_id')
      screen.GetElement(id_='sign_up_layout_id').GetElement(id_='last_name_text_id')
      screen.GetElement(id_='sign_up_layout_id').GetElement(id_='sign_up_button_id')
  
      if return_phone_enter:
        return session_info, screen_info
  
      # Enter phone number.
      screen_update = fase_model.ScreenUpdate([['sign_up_layout_id', 'phone_number_text_id'],
                                               ['sign_up_layout_id', 'first_name_text_id'],
                                               ['sign_up_layout_id', 'last_name_text_id']], [phone_number,
                                                                                             first_name,
                                                                                             last_name])
      fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
      # Click on Sign Up button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_up_layout_id', 'sign_up_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
    
    # Check.
    self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='enter_activation_layout_id').GetElement(id_='activation_code_text_id')
    screen.GetElement(id_='enter_activation_layout_id').GetElement(id_='send_button_id')
  
    if return_activation_code_enter:
      return session_info, screen_info

    # Enter activation code.
    screen_update = fase_model.ScreenUpdate(
        [['enter_activation_layout_id', 'activation_code_text_id']],
        [str(activation_code_generator.ActivationCodeGeneratorInterface.Get().codes[-1])])
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Send button.
    fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['enter_activation_layout_id', 'send_button_id']), session_info, screen_info)
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    user_id_to_user = fase_database.FaseDatabaseInterface.Get().GetUserIdToUser()
    self.assertEqual(1, len(user_id_to_user))
    actual_user_id = list(user_id_to_user.keys())[0]
    if expected_user_id is None:
      expected_user_id = actual_user_id 
    else:
      self.assertEqual(expected_user_id, actual_user_id)
    # Check present of main elements.
    fase_database.FaseDatabaseInterface.Get().GetService(expected_user_id)
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(expected_user_id)
    self.assertEqual(session_info.session_id, screen.GetElement(id_='user_id_before_label_id').GetLabel())

  def testSignIn_Existing_Service_Screen_User(self):
    service = SignInTestService()
    service._session_id = '321'
    screen = service.OnStart()
    screen = service.OnAbount(screen, screen.GetElement(id_='about_button_id'))

    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[service],
            screen_list=[screen],
            user_list=[
                fase_model.User(user_id='321',
                                phone_number='+13216549870',
                                first_name='Edward',
                                last_name='Igushev',
                                datetime_added=datetime.datetime.now())]),
        overwrite=True)

    self.SignInProcedure(service_num_before=2, screen_num_before=2,
                         service_num_during=2, screen_num_during=3,
                         sign_in=True,
                         phone_number='+13216549870',
                         expected_user_id='321')

  def testSignIn_Non_Existing_Service_Screen_Existing_User(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[
                fase_model.User(user_id='321',
                                phone_number='+13216549870',
                                first_name='Edward',
                                last_name='Igushev',
                                datetime_added=datetime.datetime.now())]),
        overwrite=True)

    self.SignInProcedure(service_num_before=1, screen_num_before=1,
                         service_num_during=1, screen_num_during=2,
                         sign_in=True,
                         phone_number='+13216549870',
                         expected_user_id='321')

  def testSignIn_Wrong_PhoneNumber(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[]),
        overwrite=True)

    session_info, screen_info = (
        self.SignInProcedure(service_num_before=1, screen_num_before=1,
                             service_num_during=1, screen_num_during=2,
                             sign_in=True,
                             phone_number='+13216549870',
                             return_phone_enter=True))

    # Enter phone number.
    screen_update = fase_model.ScreenUpdate([['sign_in_layout_id', 'phone_number_text_id']], ['+13216549870'])
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_in_layout_id', 'sign_in_button_id']), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check Popup window.
    self.assertEqual('User with such phone number has not been found!', screen.GetPopup().GetText())

  def testSignUp_Non_Existing_Service_Screen_User(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[]),
        overwrite=True)

    self.SignInProcedure(service_num_before=1, screen_num_before=1,
                         service_num_during=1, screen_num_during=2,
                         sign_in=False,
                         phone_number='+13216549870', first_name='Edward', last_name='Igushev')

  def testSignUp_Existing_PhoneNumber(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[
                fase_model.User(user_id='321',
                                phone_number='+13216549870',
                                first_name='Edward',
                                last_name='Igushev',
                                datetime_added=datetime.datetime.now())]),
        overwrite=True)

    session_info, screen_info = (
        self.SignInProcedure(service_num_before=1, screen_num_before=1,
                             service_num_during=1, screen_num_during=2,
                             sign_in=False,
                             phone_number='+13216549870', first_name='Edward', last_name='Igushev',
                             return_phone_enter=True))

    # Enter phone number.
    screen_update = fase_model.ScreenUpdate([['sign_up_layout_id', 'phone_number_text_id'],
                                             ['sign_up_layout_id', 'first_name_text_id'],
                                             ['sign_up_layout_id', 'last_name_text_id']], ['+13216549870',
                                                                                           'Edward',
                                                                                           'Igushev'])
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign Up button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_up_layout_id', 'sign_up_button_id']), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check Popup window.
    self.assertEqual('User with such phone number is already registered!', screen.GetPopup().GetText())

  def testSignUp_Wrong_ActivationCode(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[]),
        overwrite=True)

    session_info, screen_info = (
        self.SignInProcedure(service_num_before=1, screen_num_before=1,
                             service_num_during=1, screen_num_during=2,
                             sign_in=False,
                             phone_number='+13216549870', first_name='Edward', last_name='Igushev',
                             return_activation_code_enter=True))

    # Enter activation code.
    screen_update = fase_model.ScreenUpdate([['enter_activation_layout_id', 'activation_code_text_id']], '1234')
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Send button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['enter_activation_layout_id', 'send_button_id']), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check Popup window.
    self.assertEqual('Wrong activation code!', screen.GetPopup().GetText())

  def testSignOut_Existing_Service_Screen_User(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[]),
        overwrite=True)

    # Create Service.
    response = fase_server.FaseServer.Get().GetService(fase_model.Device(device_type='iOS', device_token='Token'))
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen

    fase_database.FaseDatabaseInterface.Get().AddUser(
        fase_model.User(user_id=session_info.session_id,
                        phone_number='+13216549870',
                        first_name='Edward',
                        last_name='Igushev',
                        datetime_added=datetime.datetime.now()))

    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetUserIdToUser()))
    # Check present of main elements.
    screen.GetElement(id_='sign_out_button_id')

    # Click on Sign Out button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_out_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='sign_out_layout_id').GetElement(id_='sign_out_button_id')

    # Click on Sign Out button.
    fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_out_layout_id', 'sign_out_button_id']), session_info, screen_info)

    # Check.
    session_id_to_service = fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()
    self.assertEqual(2, len(session_id_to_service))
    self.assertIn(session_info.session_id, session_id_to_service)
    actual_service_session_id = list(set(session_id_to_service.keys()) - {session_info.session_id})[0]

    session_id_to_screen = fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()
    self.assertEqual(2, len(session_id_to_screen))
    self.assertIn(session_info.session_id, session_id_to_screen)
    actual_screen_session_id = list(set(session_id_to_screen.keys()) - {session_info.session_id})[0]

    user_id_to_user = fase_database.FaseDatabaseInterface.Get().GetUserIdToUser()
    self.assertEqual(1, len(user_id_to_user))
    actual_user_id = list(user_id_to_user.keys())[0]

    self.assertEqual(actual_screen_session_id, actual_service_session_id)
    self.assertNotEqual(actual_user_id, actual_service_session_id)
    
    # Check present of main elements.
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(actual_service_session_id)
    screen.GetElement(id_='sign_out_button_id')

  def testSkip(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[]),
        overwrite=True)

    # Create Service.
    response = fase_server.FaseServer.Get().GetService(fase_model.Device(device_type='iOS', device_token='Token'))
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='sign_in_button_id')

    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_in_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_in_button_id')
    screen.GetElement(id_='sign_in_layout_id').GetElement(id_='sign_up_button_id')
    
    # Click on Skip button
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_in_layout_id', 'skip_button_id']), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen.GetElement(id_='about_button_id')


if __name__ == '__main__':
    unittest.main()
