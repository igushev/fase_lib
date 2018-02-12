import unittest

import fase_database
import fase_model
import fase_server
import fase
import hello_world


class FaseServerTest(unittest.TestCase):

  def setUp(self):
    super(FaseServerTest, self).setUp()
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_prog_list=[], user_list=[]), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def testRemoveVariablesFromElement(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, _ = self._GetServiceAndAssert(device)
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen = fase.Screen(service)
    frame = screen.AddFrame(id_='frame_id')
    frame.AddText(id_='text_id')
    frame.AddStringVariable(id_='value_str', value='general')
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='value_str'))
    screen_removed_variables = fase_server.RemoveVariablesFromElement(screen)
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='value_str'))
    self.assertTrue(screen_removed_variables.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertFalse(screen_removed_variables.GetElement(id_='frame_id').HasElement(id_='value_str'))

  def testSendInternalCommand(self):
    command = fase_model.Command(fase_server.CREATE_DB_COMMAND)
    status = fase_server.FaseServer.Get().SendInternalCommand(command)
    self.assertEqual(fase_server.TABLES_CREATED, status.message)

    command = fase_model.Command(fase_server.DELETE_DB_COMMAND)
    status = fase_server.FaseServer.Get().SendInternalCommand(command)
    self.assertEqual(fase_server.TABLES_DELETED, status.message)

  def testSendInternalCommandError(self):
    command = fase_model.Command('FAKE_COMMAND')
    self.assertRaises(fase_server.BadRequestException, fase_server.FaseServer.Get().SendInternalCommand, command)

  def testSendServiceCommand(self):
    command = fase_model.Command('ServiceName')
    status = fase_server.FaseServer.Get().SendServiceCommand(command)
    self.assertEqual('HelloWorld', status.message)

  @staticmethod
  def _GetEnterNameScreen(service, name=None):
    screen = fase.Screen(service)
    screen.AddText(id_='text_name_id', hint='Enter Name', text=name)
    screen.AddButton(id_='next_button_id', text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    return screen

  @staticmethod
  def _GetGreetingScreen(service, name):
    screen = fase.Screen(service)
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id',text='Reset', on_click=hello_world.HelloWorldService.OnResetButton)
    return screen

  def _GetScreenProgAndAssert(self, session_info,
                              expected_screen=None,
                              expected_elements_update=None,
                              expected_device=None):
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    self.assertEqual(expected_screen, screen_prog.screen)
    self.assertEqual(expected_elements_update, screen_prog.elements_update)
    self.assertEqual(expected_device, screen_prog.recent_device)

  def _GetScreenAndAssert(self, device, session_info, screen_info, expected_screen=None, expected_elements_update=None):
    response = fase_server.FaseServer.Get().GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)
    self.assertEqual(expected_elements_update, response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

  def _GetServiceAndAssert(self, device, get_screen_and_assert=True):
    response = fase_server.FaseServer.Get().GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    self.assertIsNone(response.elements_update)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen)
    return session_info, screen_info

  def _EnterNameAndAssert(self, name, device, session_info, screen_info, get_screen_and_assert=True):
    elements_update=fase_model.ElementsUpdate([['text_name_id']], [name])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response = fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service, name=name)
    expected_screen._screen_id = screen_info.screen_id
    self.assertIsNone(response.screen)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

    self._GetScreenProgAndAssert(session_info,
                                 expected_screen=expected_screen,
                                 expected_elements_update=elements_update,
                                 expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen)

  def _EnterNextAndAssert(self, name, device, session_info, screen_info, get_screen_and_assert=True):
    element_clicked = fase_model.ElementClicked(id_list=['next_button_id'], device=device)
    response = fase_server.FaseServer.Get().ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service, name)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen)
    return screen_info

  def _EnterResetAndAssert(self, device, session_info, screen_info, get_screen_and_assert=True):
    element_clicked = fase_model.ElementClicked(id_list=['reset_button_id'], device=device)
    response = fase_server.FaseServer.Get().ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen)
    return screen_info

  def testHelloWorld(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info)
    screen_info = self._EnterNextAndAssert('Henry Ford', device, session_info, screen_info)
    self._EnterResetAndAssert(device, session_info, screen_info)

  def testHelloWorldElementClickedWithElementsUpdate(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Henry Ford'])
    element_clicked = fase_model.ElementClicked(
        elements_update=elements_update, id_list=['next_button_id'], device=device)
    response = fase_server.FaseServer.Get().ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service, 'Henry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen)
    
    self._EnterResetAndAssert(device, session_info, screen_info)

  def testHelloWorldElementClickedWithDiffDevice(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info)
    device_2 = fase_model.Device('MockType', 'MockToken2')
    screen_info = self._EnterNextAndAssert('Henry Ford', device_2, session_info, screen_info)
    self._EnterResetAndAssert(device_2, session_info, screen_info)

  def testHelloWorldUpdateElementsUpdate(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info)
    self._EnterNameAndAssert('Howard Hughes', device, session_info, screen_info)

  def testHelloWorldUpdateElementsEmpty(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)
    # Enter name and assert update in database.
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    expected_elements_update = fase_model.ElementsUpdate([['text_name_id']], ['Henry Ford']) 
    self.assertEqual(expected_elements_update, screen_prog.elements_update)
    # Clean name and assert update has been deleted from database.
    elements_update=fase_model.ElementsUpdate([['text_name_id']], [''])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    expected_elements_update = fase_model.ElementsUpdate([['text_name_id']], ['']) 
    self.assertEqual(expected_elements_update, screen_prog.elements_update)

  def testHelloWorldScreenUpdateWithDiffDevice(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info)
    
    device_2 = fase_model.Device('MockType', 'MockToken2')
    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device_2)
    response = fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service, name='Howard Hughes')
    expected_screen._screen_id = screen_info.screen_id
    self.assertIsNone(response.screen)
    self.assertEqual(elements_update, response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

    self._GetScreenProgAndAssert(session_info,
                                 expected_screen=expected_screen,
                                 expected_elements_update=elements_update,
                                 expected_device=device_2)
    self._GetScreenAndAssert(device_2, session_info, screen_info, expected_screen=expected_screen)

  def testHelloWorldElementClickedScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert('Henry Ford', device, session_info, screen_info_entered_name)

    screen_prog_clicked_next = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_clicked_next = screen_prog_clicked_next.screen 

    element_clicked = fase_model.ElementClicked(id_list=['next_button_id'], device=device)
    response_click_again = fase_server.FaseServer.Get().ElementClicked(
        element_clicked, session_info, screen_info_entered_name)
    self.assertEqual(screen_clicked_next, response_click_again.screen)
    self.assertIsNone(response_click_again.elements_update)
    self.assertEqual(session_info, response_click_again.session_info)
    self.assertEqual(screen_info_clicked_next, response_click_again.screen_info)

  def testHelloWorldScreenUpdateScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert('Henry Ford', device, session_info, screen_info_entered_name)

    screen_prog_clicked_next = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_clicked_next = screen_prog_clicked_next.screen 

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response_enter_name_again = fase_server.FaseServer.Get().ScreenUpdate(
        screen_update, session_info, screen_info_entered_name)
    self.assertEqual(screen_clicked_next, response_enter_name_again.screen)
    self.assertIsNone(response_enter_name_again.elements_update)
    self.assertEqual(session_info, response_enter_name_again.session_info)
    self.assertEqual(screen_info_clicked_next, response_enter_name_again.screen_info)


if __name__ == '__main__':
    unittest.main()
