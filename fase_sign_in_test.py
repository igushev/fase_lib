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
    screen = fase.Screen()
    screen.AddButton(id_='sign_in_button_id',
                     text='Sign In', on_click=SignInTestService.OnSignIn)
    screen.AddButton(id_='about_button_id',
                     text='Abount', on_click=SignInTestService.OnAbount)
    return screen

  def OnSignIn(self, screen, element):
    return fase_sign_in.FaseSignIn.Start(self, on_sign_in_done=SignInTestService.OnSignInDone, cancel_option=True)

  def OnSignInDone(self, cancelled=False, skipped=False, user_id_before=None):
    screen = fase.Screen()
    screen.AddLabel(id_='user_id_before_label_id', label=user_id_before)
    return screen

  def OnAbount(self, screen, element):
    screen = fase.Screen()
    screen.AddLabel(id_='about_label_id', label='Sign In Test Service')
    return screen

fase.Service.RegisterService(SignInTestService)


class FaseSignInTest(unittest.TestCase):

  def setUp(self):
    activation_code_generator.ActivationCodeGeneratorInterface.Set(
        activation_code_generator.MockActivationCodeGenerator(activation_code_generator.ActivationCodeGenerator()))
    sms_sender.SMSSender.Set(sms_sender.SMSSender(sms_sender.MockSMSServiceProvider()))

    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[],
            screen_list=[],
            user_list=[
                fase_model.User(user_id='321',
                                phone_number='+13216549870',
                                first_name='Edward',
                                last_name='Igushev',
                                display_name='Edward Igushev',
                                device=fase_model.Device(device_type='iOS',
                                                         device_token='Token'),
                                datetime_added=datetime.datetime.now())]))

    service = SignInTestService()
    service._session_id = '321'
    screen = service.OnStart()
    screen = service.OnAbount(screen, screen.GetElement(id_='about_button_id'))
    fase_database.FaseDatabaseInterface.Get().AddService(service)
    screen._session_id = service._session_id
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen)

  def testSingIn(self):
    # Create Server and Service.
    fase_server_ = fase_server.FaseServer()
    session_info = fase_server_.GetService(fase_model.Device(device_type='iOS',
                                                             device_token='Token'))
    fase_server_.GetScreen(session_info)

    # Check.
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_info.session_id)
    screen.GetElement('sign_in_button_id')

    # Click on Sign In button.
    fase_server_.ElementClicked(fase_model.ElementClicked(['sign_in_button_id']), session_info)
    
    # Check.
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(3, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_info.session_id)
    screen.GetElement('sign_in_layout_id').GetElement(id_='sign_in_button_id')
    screen.GetElement('sign_in_layout_id').GetElement(id_='sign_up_button_id')

    # Click on Sign In button.
    fase_server_.ElementClicked(fase_model.ElementClicked(['sign_in_layout_id', 'sign_in_button_id']), session_info)

    # Check.
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(3, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_info.session_id)
    screen.GetElement('sign_in_layout_id').GetElement(id_='phone_number_text_id')
    screen.GetElement('sign_in_layout_id').GetElement(id_='sign_in_button_id')

    # Enter phone number.
    screen_update = fase_model.ScreenUpdate([['sign_in_layout_id', 'phone_number_text_id']], ['+13216549870'])
    fase_server_.ScreenUpdate(screen_update, session_info)
    # Click on Sign In button.
    fase_server_.ElementClicked(fase_model.ElementClicked(['sign_in_layout_id', 'sign_in_button_id']), session_info)
    
    # Check.
    self.assertEqual(2, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(3, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen(session_info.session_id)
    screen.GetElement('enter_activation_layout_id').GetElement(id_='activation_code_text_id')
    screen.GetElement('enter_activation_layout_id').GetElement(id_='send_button_id')

    # Enter phone number.
    screen_update = fase_model.ScreenUpdate(
        [['enter_activation_layout_id', 'activation_code_text_id']],
        [str(activation_code_generator.ActivationCodeGeneratorInterface.Get().codes[-1])])
    fase_server_.ScreenUpdate(screen_update, session_info)
    # Click on Send button.
    fase_server_.ElementClicked(fase_model.ElementClicked(['enter_activation_layout_id', 'send_button_id']), session_info)
    
    # Check.
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToService()))
    self.assertEqual(1, len(fase_database.FaseDatabaseInterface.Get().GetSessionIdToScreen()))
    # Check present of main elements.
    session = fase_database.FaseDatabaseInterface.Get().GetService('321')
    screen = fase_database.FaseDatabaseInterface.Get().GetScreen('321')
    self.assertEqual(session_info.session_id,
                     screen.GetElement('user_id_before_label_id').GetLabel())


if __name__ == '__main__':
    unittest.main()
