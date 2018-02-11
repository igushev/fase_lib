import datetime
import unittest

import activation_code_generator
import fase_database
import fase_model
import fase_server
import fase_sign_in
import fase
import sms_sender

COUNTRY_CODE = 'US'


class SignInTestService(fase.Service):

  service_id = 'SignInTest'

  @staticmethod
  def GetServiceId():
    return SignInTestService.service_id

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddButton(id_='sign_in_button_id',
                     text='Sign In', on_click=SignInTestService.OnSignIn)
    screen.AddButton(id_='about_button_id',
                     text='About', on_click=SignInTestService.OnAbount)
    return screen

  request_user_data = None

  def OnSignIn(self, screen, element):
    return fase_sign_in.StartSignIn(
        self, on_done=SignInTestService.OnSignInDone, on_skip=SignInTestService.OnSignInSkip,
        on_cancel=SignInTestService.OnSignInCancel, request_user_data=SignInTestService.request_user_data)

  def OnSignOut(self, screen, element):
    return fase_sign_in.StartSignOut(self)

  def OnSignInDone(self, user_id_before=None):
    screen = fase.Screen(self)
    screen.AddLabel(id_='user_id_before_label_id', text=user_id_before)
    screen.AddButton(id_='sign_out_button_id',
                     text='Sign Out', on_click=SignInTestService.OnSignOut)
    return screen

  def OnSignInSkip(self):
    screen = fase.Screen(self)
    screen.AddLabel(id_='skip_label', text='Sign In Skipped')
    return screen

  def OnSignInCancel(self):
    screen = fase.Screen(self)
    screen.AddLabel(id_='cancel_label', text='Sign In Cancelled')
    return screen

  def OnAbount(self, screen, element):
    screen = fase.Screen(self)
    screen.AddLabel(id_='about_label_id', text='Sign In Test Service')
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
                      service_num_after, screen_num_after,
                      sign_in=None,
                      phone_number=None, first_name=None, last_name=None,
                      date_of_birth=None, home_city=None,
                      expected_user_id=None,
                      request_user_data=None,
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
    self.assertEqual(screen_num_before, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check present of main elements.
    screen.GetElement(id_='sign_in_button_id')

    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_in_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check present of main elements.
    screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_in_button_id')
    screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_up_button_id')

    if sign_in:
      # Click on Sign In button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_frame_id', 'sign_in_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
      # Check.
      self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
      # Check present of main elements.
      screen.GetElement(id_='sign_in_frame_id').GetElement(id_='phone_number_text_id')
      screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_in_button_id')
  
      if return_phone_enter:
        return response
  
      # Enter phone number.
      elements_update=fase_model.ElementsUpdate([['sign_in_frame_id', 'phone_number_text_id']], [phone_number])
      screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
      fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
      # Click on Sign In button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_frame_id', 'sign_in_button_id'],
                                    locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
      
      if request_user_data is not None:
        # Check.
        self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
        self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
        # Check present of main elements.
        if request_user_data.date_of_birth:
          self.assertEqual(request_user_data.date_of_birth,
                           screen.GetElement(id_='enter_frame_id').HasElement(id_='date_of_birth_date_picker'))
          self.assertEqual(
              request_user_data.home_city,
              screen.GetElement(id_='enter_frame_id').HasElement(id_='fase_sign_in_request_user_data_home_city'))
    
        # Enter Requested User Data.
        id_list_list = []
        value_list = []
        if request_user_data.date_of_birth:
          id_list_list.append(['enter_frame_id', 'date_of_birth_date_picker'])
          value_list.append(date_of_birth.strftime(fase.DATETIME_FORMAT))
        if request_user_data.home_city:
          id_list_list.append(['enter_frame_id', 'home_city_place_picker'])
          value_list.append(home_city.Get())
        elements_update = fase_model.ElementsUpdate(id_list_list, value_list)
        screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
        fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
        # Click on Enter button.
        response = fase_server.FaseServer.Get().ElementClicked(
            fase_model.ElementClicked(id_list=['enter_frame_id', 'enter_button_id'],
                                      locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
        screen_info = response.screen_info
        screen = response.screen

    else:
      # Click on Sign Up button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_frame_id', 'sign_up_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
      # Check.
      self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
      # Check present of main elements.
      screen.GetElement(id_='sign_up_frame_id').GetElement(id_='phone_number_text_id')
      screen.GetElement(id_='sign_up_frame_id').GetElement(id_='first_name_text_id')
      screen.GetElement(id_='sign_up_frame_id').GetElement(id_='last_name_text_id')
      screen.GetElement(id_='sign_up_frame_id').GetElement(id_='sign_up_button_id')
  
      if return_phone_enter:
        return response
  
      # Enter phone number.
      elements_update = fase_model.ElementsUpdate([['sign_up_frame_id', 'phone_number_text_id'],
                                                   ['sign_up_frame_id', 'first_name_text_id'],
                                                   ['sign_up_frame_id', 'last_name_text_id']], [phone_number,
                                                                                                 first_name,
                                                                                                 last_name])
      screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
      fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
      # Click on Sign Up button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_up_frame_id', 'sign_up_button_id'],
                                    locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen

    # Check.
    self.assertEqual(service_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(screen_num_during, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check present of main elements.
    screen.GetElement(id_='enter_activation_frame_id').GetElement(id_='activation_code_text_id')
    screen.GetElement(id_='enter_activation_frame_id').GetElement(id_='send_button_id')
  
    if return_activation_code_enter:
      return response

    # Assign user_id before entering activation code.
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    user_id_before = service.GetUserId()

    # Enter activation code.
    elements_update=fase_model.ElementsUpdate(
        [['enter_activation_frame_id', 'activation_code_text_id']],
        [str(activation_code_generator.ActivationCodeGeneratorInterface.Get().codes[-1])])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Send button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['enter_activation_frame_id', 'send_button_id']), session_info, screen_info)
    screen_info = response.screen_info
    screen = response.screen
    # Check.
    self.assertEqual(service_num_after, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(screen_num_after, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    user_id_to_user = fase_database.FaseDatabaseInterface.Get().GetUserIdToUser()
    self.assertEqual(1, len(user_id_to_user))
    actual_user_id = list(user_id_to_user.keys())[0]
    if expected_user_id is None:
      expected_user_id = actual_user_id 
    else:
      self.assertEqual(expected_user_id, actual_user_id)
    # Check present of main elements.
    screen.GetElement(id_='user_id_before_label_id')
    # Assert user_id_before equal to actual user_id before entering the activation code.
    self.assertEqual(user_id_before, screen.GetElement(id_='user_id_before_label_id').GetText())
    return response

  def testSignIn_Existing_Service_Screen_User(self):
    user = fase.User(user_id='321',
                     phone_number='+13216549870',
                     first_name='Edward',
                     last_name='Igushev',
                     datetime_added=datetime.datetime.now())
    service = SignInTestService()
    service._session_id = fase_sign_in.GenerateSignedInSessionId(user.user_id)
    screen = service.OnStart()
    screen = service.OnAbount(screen, screen.GetElement(id_='about_button_id'))
    screen_prog = fase_model.ScreenProg(session_id=service.GetSessionId(), screen=screen)

    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[service],
            screen_prog_list=[screen_prog],
            user_list=[user]),
        overwrite=True)

    self.SignInProcedure(service_num_before=2, screen_num_before=2,
                         service_num_during=2, screen_num_during=2,
                         service_num_after=1, screen_num_after=1,
                         sign_in=True,
                         phone_number='+13216549870',
                         expected_user_id='321')

  def testSignIn_Non_Existing_Service_Screen_Existing_User(self):
    user = fase.User(user_id='321',
                     phone_number='+13216549870',
                     first_name='Edward',
                     last_name='Igushev',
                     datetime_added=datetime.datetime.now())
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[user]),
        overwrite=True)

    self.SignInProcedure(service_num_before=1, screen_num_before=1,
                         service_num_during=1, screen_num_during=1,
                         service_num_after=1, screen_num_after=1,
                         sign_in=True,
                         phone_number='+13216549870',
                         expected_user_id='321')

  def testSignIn_Wrong_PhoneNumber(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[]),
        overwrite=True)

    response = self.SignInProcedure(service_num_before=1, screen_num_before=1,
                                    service_num_during=1, screen_num_during=1,
                                    service_num_after=1, screen_num_after=1,
                                    sign_in=True,
                                    phone_number='+13216549870',
                                    return_phone_enter=True)
    session_info = response.session_info
    screen_info = response.screen_info

    # Enter phone number.
    elements_update=fase_model.ElementsUpdate([['sign_in_frame_id', 'phone_number_text_id']], ['+13216549870'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign In button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_in_frame_id', 'sign_in_button_id'],
                                  locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check Alert window.
    self.assertEqual('User with such phone number has not been found!', screen.GetAlert().GetText())

  def testSignUp_Non_Existing_Service_Screen_User(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[]),
        overwrite=True)

    self.SignInProcedure(service_num_before=1, screen_num_before=1,
                         service_num_during=1, screen_num_during=1,
                         service_num_after=1, screen_num_after=1,
                         sign_in=False,
                         phone_number='+13216549870', first_name='Edward', last_name='Igushev')

  def testSignUp_Existing_PhoneNumber(self):
    user = fase.User(user_id='321',
                     phone_number='+13216549870',
                     first_name='Edward',
                     last_name='Igushev',
                     datetime_added=datetime.datetime.now())
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[user]),
        overwrite=True)

    response = self.SignInProcedure(service_num_before=1, screen_num_before=1,
                                    service_num_during=1, screen_num_during=1,
                                    service_num_after=1, screen_num_after=1,
                                    sign_in=False,
                                    phone_number='+13216549870', first_name='Edward', last_name='Igushev',
                                    return_phone_enter=True)
    session_info = response.session_info
    screen_info = response.screen_info

    # Enter phone number.
    elements_update=fase_model.ElementsUpdate([['sign_up_frame_id', 'phone_number_text_id'],
                                               ['sign_up_frame_id', 'first_name_text_id'],
                                               ['sign_up_frame_id', 'last_name_text_id']], ['+13216549870',
                                                                                             'Edward',
                                                                                             'Igushev'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Sign Up button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_up_frame_id', 'sign_up_button_id'],
                                  locale=fase.Locale(country_code=COUNTRY_CODE)), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check Alert window.
    self.assertEqual('User with such phone number is already registered!', screen.GetAlert().GetText())

  def testSignUp_Wrong_ActivationCode(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[]),
        overwrite=True)

    response = self.SignInProcedure(service_num_before=1, screen_num_before=1,
                                    service_num_during=1, screen_num_during=1,
                                    service_num_after=1, screen_num_after=1,
                                    sign_in=False,
                                    phone_number='+13216549870', first_name='Edward', last_name='Igushev',
                                    return_activation_code_enter=True)
    session_info = response.session_info
    screen_info = response.screen_info

    # Enter activation code.
    elements_update=fase_model.ElementsUpdate([['enter_activation_frame_id', 'activation_code_text_id']], '1234')
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    # Click on Send button.
    response = fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['enter_activation_frame_id', 'send_button_id']), session_info, screen_info)
    screen = response.screen
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check Alert window.
    self.assertEqual('Wrong activation code!', screen.GetAlert().GetText())

  def testSignOut_Existing_Service_Screen_User(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[]),
        overwrite=True)

    # Sign Up and create service.
    response = self.SignInProcedure(service_num_before=1, screen_num_before=1,
                                    service_num_during=1, screen_num_during=1,
                                    service_num_after=1, screen_num_after=1,
                                    sign_in=False,
                                    phone_number='+13216549870', first_name='Edward', last_name='Igushev')
    session_info = response.session_info
    screen_info = response.screen_info
    screen = response.screen

    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
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
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
    # Check present of main elements.
    screen.GetElement(id_='sign_out_frame_id').GetElement(id_='sign_out_button_id')

    # Click on Sign Out button.
    fase_server.FaseServer.Get().ElementClicked(
        fase_model.ElementClicked(id_list=['sign_out_frame_id', 'sign_out_button_id']), session_info, screen_info)

    # Check.
    session_id_to_service = fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()
    self.assertEqual(2, len(session_id_to_service))
    self.assertIn(session_info.session_id, session_id_to_service)
    actual_service_session_id = list(set(session_id_to_service.keys()) - {session_info.session_id})[0]

    session_id_to_screen_prog = fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()
    self.assertEqual(2, len(session_id_to_screen_prog))
    self.assertIn(session_info.session_id, session_id_to_screen_prog)
    actual_screen_session_id = list(set(session_id_to_screen_prog.keys()) - {session_info.session_id})[0]

    user_id_to_user = fase_database.FaseDatabaseInterface.Get().GetUserIdToUser()
    self.assertEqual(1, len(user_id_to_user))
    actual_user_id = list(user_id_to_user.keys())[0]

    self.assertEqual(actual_screen_session_id, actual_service_session_id)
    self.assertNotEqual(actual_user_id, actual_service_session_id)
    
    # Check present of main elements.
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(actual_service_session_id)
    screen_prog.screen.GetElement(id_='sign_in_button_id')

  def testRequestUserData(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_prog_list=[],
            user_list=[]),
        overwrite=True)

    # Sign Up and create service.
    self.SignInProcedure(service_num_before=1, screen_num_before=1,
                         service_num_during=1, screen_num_during=1,
                         service_num_after=1, screen_num_after=1,
                         sign_in=False,
                         phone_number='+13216549870', first_name='Edward', last_name='Igushev')

    service_id_bck = SignInTestService.service_id
    request_user_data_bck = SignInTestService.request_user_data

    # Request with Date of Birth.
    SignInTestService.service_id = 'SignInTest_DateOfBirth'
    SignInTestService.request_user_data = fase.RequestUserData(date_of_birth=True)

    # Sign In Procedure must request Date of Birth. 
    self.SignInProcedure(service_num_before=2, screen_num_before=2,
                         service_num_during=2, screen_num_during=2,
                         service_num_after=2, screen_num_after=2,
                         sign_in=True,
                         phone_number='+13216549870',
                         date_of_birth=datetime.datetime(year=1986, month=5, day=22),
                         request_user_data=fase.RequestUserData(date_of_birth=True))

    SignInTestService.service_id = 'SignInTest_DateOfBirth_Second'

    # Date of Birth has been entered. 
    self.SignInProcedure(service_num_before=3, screen_num_before=3,
                         service_num_during=3, screen_num_during=3,
                         service_num_after=3, screen_num_after=3,
                         sign_in=True,
                         phone_number='+13216549870')

    # Request with Date of Birth and Home City.
    SignInTestService.service_id = 'SignInTest_DateOfBirth_HomeCity'
    SignInTestService.request_user_data = fase.RequestUserData(date_of_birth=True,
                                                               home_city=True)

    # Sign In Procedure must request HomeCity only since Date of Birth has been entered. 
    self.SignInProcedure(service_num_before=4, screen_num_before=4,
                         service_num_during=4, screen_num_during=4,
                         service_num_after=4, screen_num_after=4,
                         sign_in=True,
                         phone_number='+13216549870',
                         home_city=fase.Place(google_place_id='new-york-city-id'),
                         request_user_data=fase.RequestUserData(home_city=True))

    SignInTestService.service_id = 'SignInTest_DateOfBirth_HomeCity_Second'

    # Both Date of Birth and HomeCity has been entered.
    self.SignInProcedure(service_num_before=5, screen_num_before=5,
                         service_num_during=5, screen_num_during=5,
                         service_num_after=5, screen_num_after=5,
                         sign_in=True,
                         phone_number='+13216549870')
    
    SignInTestService.service_id = service_id_bck
    SignInTestService.request_user_data = request_user_data_bck 

  def testSkipCancel(self):
    for element_clicked_id_list, expected_element_id in [(['sign_in_frame_id', 'skip_button_id'], 'skip_label'),
                                                         ([fase.PREV_STEP_BUTTON_ID], 'cancel_label')]:
      fase_database.FaseDatabaseInterface.Set(
          fase_database.MockFaseDatabase(
              service_list=[],
              screen_prog_list=[],
              user_list=[]),
          overwrite=True)
  
      # Create Service.
      response = fase_server.FaseServer.Get().GetService(fase_model.Device(device_type='iOS', device_token='Token'))
      session_info = response.session_info
      screen_info = response.screen_info
      screen = response.screen
      # Check.
      self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
      # Check present of main elements.
      screen.GetElement(id_='sign_in_button_id')
  
      # Click on Sign In button.
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=['sign_in_button_id']), session_info, screen_info)
      screen_info = response.screen_info
      screen = response.screen
      # Check.
      self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
      # Check present of main elements.
      screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_in_button_id')
      screen.GetElement(id_='sign_in_frame_id').GetElement(id_='sign_up_button_id')
      
      # Click on Skip button
      response = fase_server.FaseServer.Get().ElementClicked(
          fase_model.ElementClicked(id_list=element_clicked_id_list), session_info, screen_info)
      screen = response.screen
      # Check.
      self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
      self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreenProg()))
      # Check present of main elements.
      screen.GetElement(id_=expected_element_id)


if __name__ == '__main__':
    unittest.main()
