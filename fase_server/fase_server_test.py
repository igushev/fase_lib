import unittest

import fase_database
from fase_model import fase_model
import fase_server
from fase import fase


class ServerTestService(fase.Service):

  @staticmethod
  def ServiceCommand(command):
    if command.command == 'ServiceName':
      return 'HelloWorld'
    else:
      raise AssertionError('Wrong ServiceCommand') 

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddImage(id_='image_id', filename='/logo.png')
    screen.AddText(id_='text_name_id', hint='Enter Name')
    screen.AddButton(id_='next_button_id',
                     text='Next', on_click=ServerTestService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetText(id_='text_name_id').GetText()
    screen = fase.Screen(self)
    screen.AddImage(id_='image_id', filename='/hello.png')
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id',
                     text='Reset', on_click=ServerTestService.OnResetButton)
    return screen
    
  def OnResetButton(self, screen, element):
    # Ignore previous screen and element.
    return self.OnStart()


fase.Service.RegisterService(ServerTestService)


class FaseServerTest(unittest.TestCase):

  def setUp(self):
    super(FaseServerTest, self).setUp()
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_prog_list=[], user_list=[]), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def testPrepareScreenNoVariables(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, _ = self._GetServiceAndAssert(device)
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen = fase.Screen(service)
    frame = screen.AddFrame(id_='frame_id')
    frame.AddText(id_='text_id')
    frame.AddStringVariable(id_='value_str', value='general')
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='value_str'))
    screen_removed_variables, _ = fase_server.PrepareScreen(screen)
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='value_str'))
    self.assertTrue(screen_removed_variables.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertFalse(screen_removed_variables.GetElement(id_='frame_id').HasElement(id_='value_str'))

  def testPrepareScreenResources(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, _ = self._GetServiceAndAssert(device)
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen = fase.Screen(service)
    frame1 = screen.AddFrame(id_='frame1_id')
    frame1.AddImage(id_='image1_id', filename='/file1')
    frame1.AddImage(id_='image2_id', filename='/file2')
    frame2 = screen.AddFrame(id_='frame2_id')
    frame2.AddImage(id_='image1_id', filename='/file1')
    frame2.AddImage(id_='image2_id', filename='/file2')
    _, resources = fase_server.PrepareScreen(screen)
    self.assertEqual(set([fase_model.Resource(filename='/file1'), fase_model.Resource(filename='/file2')]),
                     set(resources.resource_list))

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
    screen.AddImage(id_='image_id', filename='/logo.png')
    screen.AddText(id_='text_name_id', hint='Enter Name', text=name)
    screen.AddButton(id_='next_button_id', text='Next', on_click=ServerTestService.OnNextButton)
    return screen

  @staticmethod
  def _GetGreetingScreen(service, name):
    screen = fase.Screen(service)
    screen.AddImage(id_='image_id', filename='/hello.png')
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id',text='Reset', on_click=ServerTestService.OnResetButton)
    return screen

  def _GetScreenProgAndAssert(self, session_info,
                              expected_screen=None,
                              expected_elements_update=None,
                              expected_device=None):
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    self.assertEqual(expected_screen, screen_prog.screen)
    self.assertEqual(expected_elements_update, screen_prog.elements_update)
    self.assertEqual(expected_device, screen_prog.recent_device)

  def _GetScreenAndAssert(self, device, session_info, screen_info, expected_screen=None, expected_resources=None,
                          expected_elements_update=None):
    response = fase_server.FaseServer.Get().GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)
    if expected_resources is not None:
      self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    else:
      self.assertIsNone(response.resources)
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
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/logo.png')])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertIsNone(response.elements_update)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)
    return session_info, screen_info

  def _EnterNameAndAssert(self, name, device, session_info, screen_info, get_screen_and_assert=True):
    elements_update=fase_model.ElementsUpdate([['text_name_id']], [name])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response = fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service, name=name)
    expected_screen._screen_id = screen_info.screen_id
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/logo.png')])
    self.assertIsNone(response.screen)
    self.assertIsNone(response.resources)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

    self._GetScreenProgAndAssert(session_info,
                                 expected_screen=expected_screen,
                                 expected_elements_update=elements_update,
                                 expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)

  def _EnterNextAndAssert(self, name, device, session_info, screen_info, get_screen_and_assert=True):
    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response = fase_server.FaseServer.Get().ElementCallback(element_callback, session_info, screen_info)
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service, name)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/hello.png')])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)
    return screen_info

  def _EnterResetAndAssert(self, device, session_info, screen_info, get_screen_and_assert=True):
    element_callback = (
        fase_model.ElementCallback(id_list=['reset_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response = fase_server.FaseServer.Get().ElementCallback(element_callback, session_info, screen_info)
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/logo.png')])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)
    return screen_info

  def testHelloWorld(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info)
    screen_info = self._EnterNextAndAssert('Henry Ford', device, session_info, screen_info)
    self._EnterResetAndAssert(device, session_info, screen_info)

  def testHelloWorldElementCallbackWithElementsUpdate(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info = self._GetServiceAndAssert(device)

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Henry Ford'])
    element_callback = fase_model.ElementCallback(
        elements_update=elements_update, id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device)
    response = fase_server.FaseServer.Get().ElementCallback(element_callback, session_info, screen_info)
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service, 'Henry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/hello.png')])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    self._GetScreenAndAssert(device, session_info, screen_info, expected_screen=expected_screen,
                             expected_resources=expected_resources)
    
    self._EnterResetAndAssert(device, session_info, screen_info)

  def testHelloWorldElementCallbackWithDiffDevice(self):
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
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/logo.png')])
    self.assertIsNone(response.screen)
    self.assertIsNone(response.resources)
    self.assertEqual(elements_update, response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

    self._GetScreenProgAndAssert(session_info,
                                 expected_screen=expected_screen,
                                 expected_elements_update=elements_update,
                                 expected_device=device_2)
    self._GetScreenAndAssert(device_2, session_info, screen_info, expected_screen=expected_screen,
                             expected_resources=expected_resources)

  def testHelloWorldElementCallbackScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert('Henry Ford', device, session_info, screen_info_entered_name)

    screen_prog_clicked_next = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_clicked_next = screen_prog_clicked_next.screen 

    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response_click_again = fase_server.FaseServer.Get().ElementCallback(
        element_callback, session_info, screen_info_entered_name)
    self.assertEqual(screen_clicked_next, response_click_again.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/hello.png')])
    self.assertEqual(set(expected_resources.resource_list), set(response_click_again.resources.resource_list))
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
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='/hello.png')])
    self.assertEqual(set(expected_resources.resource_list), set(response_enter_name_again.resources.resource_list))
    self.assertIsNone(response_enter_name_again.elements_update)
    self.assertEqual(session_info, response_enter_name_again.session_info)
    self.assertEqual(screen_info_clicked_next, response_enter_name_again.screen_info)


if __name__ == '__main__':
    unittest.main()
