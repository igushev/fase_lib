import os
import unittest
import tempfile
import time

from fase import fase
from fase_model import fase_model

import fase_client
import fase_resource_manager

from hello_world_fase import service as hello_world_service


class MockFaseHTTPClient(object):
  
  def __init__(self, test_obj, resource_dir):
    self.test_obj = test_obj 
    self.resource_dir = resource_dir
    self.get_service_calls = 0
    self.get_screen_calls = 0
    self.screen_update_calls = 0
    self.element_callback_calls = 0
    self.get_resource_filename_calls = 0
    self.device = None
    self.service = None
    self.screen = None
    self.resources = None
    self.elements_update = None
    self.session_info = None
    self.screen_info = None
    
    self.element_callback_screen = None
    self.element_callback_resources = None
    self.element_callback_elements_update = None
    self.element_callback_session_info = None
    self.element_callback_screen_info = None
    
    self.expected_id_list = None
    self.expected_elements_update = None

  def GetService(self, device):
    self.get_service_calls += 1
    self.test_obj.assertEqual('Python', device.device_type)
    self.device = device
    return fase_model.Response(screen=self.screen,
                               resources=self.resources,
                               elements_update=self.elements_update,
                               session_info=self.session_info,
                               screen_info=self.screen_info)

  def GetScreen(self, device, session_info):
    self.get_screen_calls += 1
    self.test_obj.assertEqual('Python', device.device_type)
    self.device = device
    self.test_obj.assertEqual(fase_model.SessionInfo(self.service.GetSessionId()), session_info)
    return fase_model.Response(screen=self.screen,
                               resources=self.resources,
                               elements_update=self.elements_update,
                               session_info=self.session_info,
                               screen_info=self.screen_info)

  def ScreenUpdate(self, screen_update, session_info, screen_info):
    self.screen_update_calls += 1
    expected_screen_update = fase_model.ScreenUpdate(elements_update=self.expected_elements_update, device=self.device)
    self.test_obj.assertEqual(expected_screen_update, screen_update)
    self.test_obj.assertEqual(self.session_info, session_info)
    self.test_obj.assertEqual(self.screen_info, screen_info)
    return fase_model.Response(screen=self.screen,
                               resources=self.resources,
                               elements_update=self.elements_update,
                               session_info=self.session_info,
                               screen_info=self.screen_info)
    
  def ElementCallback(self, element_callback, session_info, screen_info):
    self.element_callback_calls += 1
    expected_element_callback = fase_model.ElementCallback(
        elements_update=self.expected_elements_update, id_list=self.expected_id_list, method=fase.ON_CLICK_METHOD,
        device=self.device)
    self.test_obj.assertEqual(expected_element_callback, element_callback)
    self.test_obj.assertEqual(self.session_info, session_info)
    self.test_obj.assertEqual(self.screen_info, screen_info)
    return fase_model.Response(screen=self.element_callback_screen,
                               resources=self.element_callback_resources,
                               elements_update=self.element_callback_elements_update,
                               session_info=self.element_callback_session_info,
                               screen_info=self.element_callback_screen_info)

  def GetResourceFilename(self, resource_dir, filename):
    open(os.path.join(self.resource_dir, filename), 'w').close()
    self.get_resource_filename_calls += 1


class MockFaseUI(object):

  def __init__(self, test_obj):
    self.test_obj = test_obj 
    self.draw_screen_calls = 0
    self.element_updated_received_calls = 0
    self.client = None
    self.expected_screen = None
    self.expected_id_list = None
    self.expected_value = None

  def SetClient(self, client):
    self.client = client

  def DrawScreen(self, screen):
    self.draw_screen_calls += 1
    self.test_obj.assertEqual(self.expected_screen, screen)

  def Run(self):
    pass

  def ElementUpdatedReceived(self, id_list, value):
    self.element_updated_received_calls += 1
    self.test_obj.assertEqual(self.expected_id_list, id_list)
    self.test_obj.assertEqual(self.expected_value, value)


class FaseServerTest(unittest.TestCase):
  
  def testGetService(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager)

    service = hello_world_service.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='a')])
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, http_client.get_resource_filename_calls)
    self.assertEqual(1, ui.draw_screen_calls)

  def testGetScreen(self):
    service = hello_world_service.HelloWorldService()

    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    session_info_tmp = tempfile.NamedTemporaryFile()
    fase_client.SaveSessionInfoIfNeeded(session_info_tmp.name, fase_model.SessionInfo(service.GetSessionId()))
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager,
                                    session_info_filepath=session_info_tmp.name)

    screen = service.OnStart()
    
    http_client.service = service
    http_client.screen = screen
    http_client.resources = fase_model.Resources(resource_list=[fase_model.Resource(filename='a')])
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_screen_calls)
    self.assertEqual(1, http_client.get_resource_filename_calls)
    self.assertEqual(1, ui.draw_screen_calls)

  def testScreenUpdateSendElementsUpdate(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager)

    service = hello_world_service.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, ui.draw_screen_calls)

    client.ElementUpdated(['text_name_id'], 'Hanry Ford')
    client.ElementUpdated(['text_name_id'], 'Howard Hughes')
    http_client.expected_elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Howard Hughes'])
    http_client.screen = None
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    client.ScreenUpdate()
    self.assertEqual(1, ui.draw_screen_calls)
    self.assertEqual(0, ui.element_updated_received_calls)

  def testScreenUpdateElementsUpdateReceived(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager)

    service = hello_world_service.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, ui.draw_screen_calls)
    
    http_client.elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Hanry Ford'])
    http_client.screen = None
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    ui.expected_id_list = ['text_name_id']
    ui.expected_value = 'Hanry Ford'
    client.ScreenUpdate()
    self.assertEqual(1, ui.draw_screen_calls)
    self.assertEqual(1, ui.element_updated_received_calls)

  def testScreenUpdateScreenReceived(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager)

    service = hello_world_service.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, ui.draw_screen_calls)
    
    screen.GetElement(id_='text_name_id').Update('Hanry Ford')
    service, screen = (
        screen.GetElement(id_='next_button_id').CallCallback(service, screen, http_client.device, fase.ON_CLICK_METHOD))
    http_client.screen = screen
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    ui.expected_screen = screen
    client.ScreenUpdate()
    self.assertEqual(2, ui.draw_screen_calls)
    self.assertEqual(0, ui.element_updated_received_calls)

  def testElementCallbackElementsUpdateReceived(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager)

    service = hello_world_service.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, ui.draw_screen_calls)
    
    http_client.elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Hanry Ford'])
    http_client.screen = None
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    screen.GetElement(id_='text_name_id').Update('Hanry Ford')
    service, element_callback_screen = (
        screen.GetElement(id_='next_button_id').CallCallback(service, screen, http_client.device, fase.ON_CLICK_METHOD))
    http_client.expected_id_list = ['next_button_id']
    http_client.element_callback_screen = element_callback_screen
    http_client.element_callback_session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.element_callback_screen_info = fase_model.ScreenInfo(element_callback_screen.GetScreenId())
    ui.expected_id_list = ['text_name_id']
    ui.expected_value = 'Hanry Ford'
    ui.expected_screen = element_callback_screen
    client.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD)
    self.assertEqual(1, http_client.element_callback_calls)
    self.assertEqual(2, ui.draw_screen_calls)
    self.assertEqual(1, ui.element_updated_received_calls)

  def testElementCallbackScreenReceived(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(self, resource_dir)
    ui = MockFaseUI(self)
    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, resource_manager=resource_manager)

    service = hello_world_service.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, ui.draw_screen_calls)
    
    screen.GetElement(id_='text_name_id').Update('Hanry Ford')
    service, screen = (
        screen.GetElement(id_='next_button_id').CallCallback(service, screen, http_client.device, fase.ON_CLICK_METHOD))
    http_client.screen = screen
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    ui.expected_screen = screen
    client.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD)
    self.assertEqual(2, ui.draw_screen_calls)
    self.assertEqual(0, ui.element_updated_received_calls)


if __name__ == '__main__':
    unittest.main()
