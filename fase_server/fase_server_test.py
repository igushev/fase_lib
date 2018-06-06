import os
import tempfile
import unittest

from server_util import resource_manager

from fase import fase
from fase_model import fase_model

import fase_database
import fase_server


class ServerTestService(fase.Service):

  @staticmethod
  def ServiceCommand(command):
    if command.command == 'ServiceName':
      return 'HelloWorld'
    else:
      raise AssertionError('Wrong ServiceCommand') 

  version = '1'

  @staticmethod
  def Version():
    return ServerTestService.version

  def OnUpdate(self):
    screen = fase.Screen(self)
    screen.AddLabel(id_='update_label_id', text='Service has been updated')
    screen.AddButton(id_='start_button_id', text='Start', on_click=ServerTestService.OnResetButton)
    return screen

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddImage(id_='image_id', filename='logo.png')
    screen.AddText(id_='text_name_id', hint='Enter Name')
    screen.AddButton(id_='next_button_id', text='Next', on_click=ServerTestService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetText(id_='text_name_id').GetText()
    screen = fase.Screen(self)
    screen.AddImage(id_='image_id', filename='hello.png')
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id', text='Reset', on_click=ServerTestService.OnResetButton)
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
            service_prog_list=[], screen_prog_list=[], user_list=[]), overwrite=True)

    dirpath = tempfile.mkdtemp()
    self.logo_filename = 'logo.png'
    open(os.path.join(dirpath, self.logo_filename), 'w').close()
    self.hello_filename = 'hello.png'
    open(os.path.join(dirpath, self.hello_filename), 'w').close()
    self.file1_filename = 'file1.png'
    open(os.path.join(dirpath, self.file1_filename), 'w').close()
    self.file2_filename = 'file2.png'
    open(os.path.join(dirpath, self.file2_filename), 'w').close()
    self.file3_filename = 'file3.png'
    self.file1_template_filename = 'file1_@.png'
    self.file1_20_filename = 'file1_2_00.png'
    open(os.path.join(dirpath, self.file1_20_filename), 'w').close()
    self.file1_30_filename = 'file1_3_00.png'
    open(os.path.join(dirpath, self.file1_30_filename), 'w').close()
    self.file2_template_filename = 'file2_@.png'
    self.file2_20_filename = 'file2_2_00.png'
    open(os.path.join(dirpath, self.file2_20_filename), 'w').close()
    self.file2_30_filename = 'file2_3_00.png'
    open(os.path.join(dirpath, self.file2_30_filename), 'w').close()
    
    resource_manager.ResourceManager.Set(resource_manager.ResourceManager(dirpath), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def testPrepareScreenNoVariables(self):
    device = fase_model.Device('MockType', 'MockToken')
    _, session_info, _ = self._GetServiceAndAssert(device)
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen = fase.Screen(service_prog.service)
    frame = screen.AddFrame(id_='frame_id')
    frame.AddText(id_='text_id')
    frame.AddStringVariable(id_='value_str', value='general')
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='value_str'))
    screen_removed_variables, _ = fase_server.PrepareScreen(screen, None)
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertTrue(screen.GetElement(id_='frame_id').HasElement(id_='value_str'))
    self.assertTrue(screen_removed_variables.GetElement(id_='frame_id').HasElement(id_='text_id'))
    self.assertFalse(screen_removed_variables.GetElement(id_='frame_id').HasElement(id_='value_str'))

  def testPrepareScreenResources(self):
    device = fase_model.Device('MockType', 'MockToken')
    _, session_info, _ = self._GetServiceAndAssert(device)
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen = fase.Screen(service_prog.service)
    frame1 = screen.AddFrame(id_='frame1_id')
    frame1.AddImage(id_='image1_id', filename=self.file1_filename)
    frame1.AddImage(id_='image2_id', filename=self.file2_filename)
    frame1.AddImage(id_='image3_id', filename=self.file3_filename)
    frame2 = screen.AddFrame(id_='frame2_id')
    frame2.AddImage(id_='image1_id', filename=self.file1_filename)
    frame2.AddImage(id_='image2_id', filename=self.file2_filename)
    frame2.AddImage(id_='image3_id', filename=self.file3_filename)
    _, resources = fase_server.PrepareScreen(screen, device)
    self.assertEqual(set([fase_model.Resource(filename=self.file1_filename),
                          fase_model.Resource(filename=self.file2_filename)]),
                     set(resources.resource_list))

  def testPrepareScreenResourcesPixelDensity(self):
    device = fase_model.Device('MockType', 'MockToken', pixel_density=1.5)
    _, session_info, _ = self._GetServiceAndAssert(device)
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen = fase.Screen(service_prog.service)
    frame = screen.AddFrame(id_='frame_id')
    frame.AddImage(id_='image1_id', filename=self.file1_template_filename)
    frame.AddImage(id_='image2_id', filename=self.file2_template_filename)
    _, resources = fase_server.PrepareScreen(screen, device)
    self.assertEqual(set([fase_model.Resource(filename=self.file1_20_filename),
                          fase_model.Resource(filename=self.file2_20_filename)]),
                     set(resources.resource_list))

    screen = fase.Screen(service_prog.service)
    frame = screen.AddFrame(id_='frame_id')
    frame.AddImage(id_='image1_id', filename=self.file1_template_filename, pixel_density_mult=2.0)
    frame.AddImage(id_='image2_id', filename=self.file2_template_filename, pixel_density_mult=2.0)
    _, resources = fase_server.PrepareScreen(screen, device)
    self.assertEqual(set([fase_model.Resource(filename=self.file1_30_filename),
                          fase_model.Resource(filename=self.file2_30_filename)]),
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
    screen.AddImage(id_='image_id', filename='logo.png')
    screen.AddText(id_='text_name_id', hint='Enter Name', text=name)
    screen.AddButton(id_='next_button_id', text='Next', on_click=ServerTestService.OnNextButton)
    return screen

  @staticmethod
  def _GetGreetingScreen(service, name):
    screen = fase.Screen(service)
    screen.AddImage(id_='image_id', filename='hello.png')
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id',text='Reset', on_click=ServerTestService.OnResetButton)
    return screen

  @staticmethod
  def _GetUpdateScreen(service):
    screen = fase.Screen(service)
    screen.AddLabel(id_='update_label_id', text='Service has been updated')
    screen.AddButton(id_='start_button_id', text='Start', on_click=ServerTestService.OnResetButton)
    return screen

  def _GetScreenProgAndAssert(self, session_info,
                              expected_screen=None,
                              expected_elements_update=None,
                              expected_device=None):
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    self.assertEqual(expected_screen, screen_prog.screen)
    self.assertEqual(expected_elements_update, screen_prog.elements_update)
    self.assertEqual(expected_device, screen_prog.recent_device)

  def _GetScreenAndAssert(self, device, version_info, session_info, screen_info, expected_screen=None,
                          expected_resources=None, expected_elements_update=None):
    response = fase_server.FaseServer.Get().GetScreen(device, version_info, session_info)
    self.assertEqual(expected_screen, response.screen)
    if expected_resources is not None:
      self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    else:
      self.assertIsNone(response.resources)
    self.assertFalse(response.resources.reset_resources)
    self.assertEqual(expected_elements_update, response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

  def _GetServiceAndAssert(self, device, get_screen_and_assert=True):
    response = fase_server.FaseServer.Get().GetService(device)
    version_info = response.version_info
    session_info = response.session_info
    screen_info = response.screen_info
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service_prog.service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.logo_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertFalse(response.resources.reset_resources)
    self.assertIsNone(response.elements_update)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, version_info, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)
    return version_info, session_info, screen_info

  def _EnterNameAndAssert(self, name, device, version_info, session_info, screen_info, get_screen_and_assert=True):
    elements_update=fase_model.ElementsUpdate([['text_name_id']], [name])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response = fase_server.FaseServer.Get().ScreenUpdate(screen_update, version_info, session_info, screen_info)
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service_prog.service, name=name)
    expected_screen._screen_id = screen_info.screen_id
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.logo_filename)])
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
      self._GetScreenAndAssert(device, version_info, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)

  def _EnterNextAndAssert(self, name, device, version_info, session_info, screen_info, get_screen_and_assert=True):
    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response = fase_server.FaseServer.Get().ElementCallback(element_callback, version_info, session_info, screen_info)
    screen_info = response.screen_info
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service_prog.service, name)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.hello_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertFalse(response.resources.reset_resources)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, version_info, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)
    return screen_info

  def _EnterResetAndAssert(self, device, version_info, session_info, screen_info, get_screen_and_assert=True):
    element_callback = (
        fase_model.ElementCallback(id_list=['reset_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response = fase_server.FaseServer.Get().ElementCallback(element_callback, version_info, session_info, screen_info)
    screen_info = response.screen_info
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service_prog.service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.logo_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertFalse(response.resources.reset_resources)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    if get_screen_and_assert:
      self._GetScreenAndAssert(device, version_info, session_info, screen_info, expected_screen=expected_screen,
                               expected_resources=expected_resources)
    return screen_info

  def testService(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info)
    screen_info = self._EnterNextAndAssert('Henry Ford', device, version_info, session_info, screen_info)
    self._EnterResetAndAssert(device, version_info, session_info, screen_info)

  def testServiceElementCallbackWithElementsUpdate(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info = self._GetServiceAndAssert(device)

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Henry Ford'])
    element_callback = fase_model.ElementCallback(
        elements_update=elements_update, id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device)
    response = fase_server.FaseServer.Get().ElementCallback(element_callback, version_info, session_info, screen_info)
    screen_info = response.screen_info
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service_prog.service, 'Henry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.hello_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response.resources.resource_list))
    self.assertFalse(response.resources.reset_resources)
    self.assertIsNone(response.elements_update)
    self.assertEqual(session_info, response.session_info)

    self._GetScreenProgAndAssert(session_info, expected_screen=expected_screen, expected_device=device)
    self._GetScreenAndAssert(device, version_info, session_info, screen_info, expected_screen=expected_screen,
                             expected_resources=expected_resources)
    
    self._EnterResetAndAssert(device, version_info, session_info, screen_info)

  def testServiceElementCallbackWithDiffDevice(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info)
    device_2 = fase_model.Device('MockType', 'MockToken2')
    screen_info = self._EnterNextAndAssert('Henry Ford', device_2, version_info, session_info, screen_info)
    self._EnterResetAndAssert(device_2, version_info, session_info, screen_info)

  def testServiceUpdateElementsUpdate(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info)
    self._EnterNameAndAssert('Howard Hughes', device, version_info, session_info, screen_info)

  def testServiceUpdateElementsEmpty(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info = self._GetServiceAndAssert(device)
    # Enter name and assert update in database.
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    expected_elements_update = fase_model.ElementsUpdate([['text_name_id']], ['Henry Ford']) 
    self.assertEqual(expected_elements_update, screen_prog.elements_update)
    # Clean name and assert update has been deleted from database.
    elements_update=fase_model.ElementsUpdate([['text_name_id']], [''])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    fase_server.FaseServer.Get().ScreenUpdate(screen_update, version_info, session_info, screen_info)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    expected_elements_update = fase_model.ElementsUpdate([['text_name_id']], ['']) 
    self.assertEqual(expected_elements_update, screen_prog.elements_update)

  def testServiceScreenUpdateWithDiffDevice(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info)
    
    device_2 = fase_model.Device('MockType', 'MockToken2')
    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device_2)
    response = fase_server.FaseServer.Get().ScreenUpdate(screen_update, version_info, session_info, screen_info)
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetEnterNameScreen(service_prog.service, name='Howard Hughes')
    expected_screen._screen_id = screen_info.screen_id
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.logo_filename)])
    self.assertIsNone(response.screen)
    self.assertIsNone(response.resources)
    self.assertEqual(elements_update, response.elements_update)
    self.assertEqual(session_info, response.session_info)
    self.assertEqual(screen_info, response.screen_info)

    self._GetScreenProgAndAssert(session_info,
                                 expected_screen=expected_screen,
                                 expected_elements_update=elements_update,
                                 expected_device=device_2)
    self._GetScreenAndAssert(device_2, version_info, session_info, screen_info, expected_screen=expected_screen,
                             expected_resources=expected_resources)

  def testServiceElementCallbackScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert(
        'Henry Ford', device, version_info, session_info, screen_info_entered_name)

    screen_prog_clicked_next = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_clicked_next = screen_prog_clicked_next.screen 

    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response_click_again = fase_server.FaseServer.Get().ElementCallback(
        element_callback, version_info, session_info, screen_info_entered_name)
    self.assertEqual(screen_clicked_next, response_click_again.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.hello_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response_click_again.resources.resource_list))
    self.assertIsNone(response_click_again.elements_update)
    self.assertEqual(session_info, response_click_again.session_info)
    self.assertEqual(screen_info_clicked_next, response_click_again.screen_info)

  def testServiceScreenUpdateScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert(
        'Henry Ford', device, version_info, session_info, screen_info_entered_name)

    screen_prog_clicked_next = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_clicked_next = screen_prog_clicked_next.screen 

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response_enter_name_again = fase_server.FaseServer.Get().ScreenUpdate(
        screen_update, version_info, session_info, screen_info_entered_name)
    self.assertEqual(screen_clicked_next, response_enter_name_again.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.hello_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response_enter_name_again.resources.resource_list))
    self.assertIsNone(response_enter_name_again.elements_update)
    self.assertEqual(session_info, response_enter_name_again.session_info)
    self.assertEqual(screen_info_clicked_next, response_enter_name_again.screen_info)

  def _AssertServiceUpdateScreen(self, response_updated, session_info):
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen_prog_updated = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_id_updated = screen_prog_updated.screen._screen_id
    expected_screen = FaseServerTest._GetUpdateScreen(service_prog.service)
    expected_screen._screen_id = screen_id_updated
    self.assertEqual(expected_screen, screen_prog_updated.screen)
    self.assertEqual(expected_screen, response_updated.screen)
    self.assertEqual([], response_updated.resources.resource_list)
    self.assertTrue(response_updated.resources.reset_resources)
    self.assertIsNone(response_updated.elements_update)
    self.assertEqual(session_info, response_updated.session_info)
    self.assertEqual(fase_model.ScreenInfo(screen_id=screen_id_updated), response_updated.screen_info)

  def testServiceGetScreenServiceVersionObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)

    previous_version = ServerTestService.version
    ServerTestService.version = '2'

    response_updated = fase_server.FaseServer.Get().GetScreen(device, version_info, session_info)
    self._AssertServiceUpdateScreen(response_updated, session_info)

    ServerTestService.version = previous_version

  def testServiceElementCallbackServiceVersionObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)

    previous_version = ServerTestService.version
    ServerTestService.version = '2'

    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response_updated = fase_server.FaseServer.Get().ElementCallback(
        element_callback, version_info, session_info, screen_info_entered_name)
    self._AssertServiceUpdateScreen(response_updated, session_info)

    ServerTestService.version = previous_version

  def testServiceScreenUpdateServiceVersionObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)

    previous_version = ServerTestService.version
    ServerTestService.version = '2'

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response_updated = fase_server.FaseServer.Get().ScreenUpdate(
        screen_update, version_info, session_info, screen_info_entered_name)
    self._AssertServiceUpdateScreen(response_updated, session_info)

    ServerTestService.version = previous_version

  def _AssertDeviceUpdateScreen(self, response_updated, session_info, screen_info_clicked_next):
    screen_info_updated = response_updated.screen_info
    self.assertEqual(screen_info_clicked_next, screen_info_updated)
    service_prog_updated = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = FaseServerTest._GetGreetingScreen(service_prog_updated.service, 'Henry Ford')
    expected_screen._screen_id = screen_info_updated.screen_id
    self.assertEqual(expected_screen, response_updated.screen)
    expected_resources = fase_model.Resources(resource_list=[fase_model.Resource(filename=self.hello_filename)])
    self.assertEqual(set(expected_resources.resource_list), set(response_updated.resources.resource_list))
    self.assertTrue(response_updated.resources.reset_resources)
    self.assertIsNone(response_updated.elements_update)
    self.assertEqual(session_info, response_updated.session_info)


  def testServiceGetScreenDeviceVersionObsolete(self):
    previous_version = ServerTestService.version
    ServerTestService.version = '2'

    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert(
        'Henry Ford', device, version_info, session_info, screen_info_entered_name)

    version_info = fase_model.VersionInfo(version=previous_version)

    response_updated = fase_server.FaseServer.Get().GetScreen(device, version_info, session_info)
    self._AssertDeviceUpdateScreen(response_updated, session_info, screen_info_clicked_next)

    ServerTestService.version = previous_version

  def testServiceElementCallbackDeviceVersionObsolete(self):
    previous_version = ServerTestService.version
    ServerTestService.version = '2'

    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert(
        'Henry Ford', device, version_info, session_info, screen_info_entered_name)

    version_info = fase_model.VersionInfo(version=previous_version)

    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response_updated = fase_server.FaseServer.Get().ElementCallback(
        element_callback, version_info, session_info, screen_info_entered_name)
    self._AssertDeviceUpdateScreen(response_updated, session_info, screen_info_clicked_next)

    ServerTestService.version = previous_version

  def testServiceScreenUpdateDeviceVersionObsolete(self):
    previous_version = ServerTestService.version
    ServerTestService.version = '2'

    device = fase_model.Device('MockType', 'MockToken')
    version_info, session_info, screen_info_entered_name = self._GetServiceAndAssert(device)
    self._EnterNameAndAssert('Henry Ford', device, version_info, session_info, screen_info_entered_name)
    screen_info_clicked_next = self._EnterNextAndAssert(
        'Henry Ford', device, version_info, session_info, screen_info_entered_name)

    version_info = fase_model.VersionInfo(version=previous_version)

    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response_updated = fase_server.FaseServer.Get().ScreenUpdate(
        screen_update, version_info, session_info, screen_info_entered_name)
    self._AssertDeviceUpdateScreen(response_updated, session_info, screen_info_clicked_next)

    ServerTestService.version = previous_version


if __name__ == '__main__':
    unittest.main()
