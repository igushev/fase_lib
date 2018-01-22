import unittest
import tempfile
import time

import hello_world
import fase_client
import fase_model


class MockFaseHTTPClient(object):
  
  def __init__(self, test_obj):
    self.test_obj = test_obj 
    self.get_service_calls = 0
    self.get_screen_calls = 0
    self.screen_update_calls = 0
    self.element_clicked_calls = 0
    self.device = None
    self.service = None
    self.screen = None
    self.elements_update = None
    self.session_info = None
    self.screen_info = None
    
    self.element_clicked_screen = None
    self.element_clicked_elements_update = None
    self.element_clicked_session_info = None
    self.element_clicked_screen_info = None
    
    self.expected_id_list = None
    self.expected_elements_update = None

  def GetService(self, device):
    self.get_service_calls += 1
    self.test_obj.assertEqual('Python', device.device_type)
    self.device = device
    return fase_model.Response(screen=self.screen,
                               elements_update=self.elements_update,
                               session_info=self.session_info,
                               screen_info=self.screen_info)

  def GetScreen(self, device, session_info):
    self.get_screen_calls += 1
    self.test_obj.assertEqual('Python', device.device_type)
    self.device = device
    self.test_obj.assertEqual(fase_model.SessionInfo(self.service.GetSessionId()), session_info)
    return fase_model.Response(screen=self.screen,
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
                               elements_update=self.elements_update,
                               session_info=self.session_info,
                               screen_info=self.screen_info)
    
  def ElementClicked(self, element_clicked, session_info, screen_info):
    self.element_clicked_calls += 1
    expected_element_clicked = fase_model.ElementClicked(
        elements_update=self.expected_elements_update, id_list=self.expected_id_list, device=self.device)
    self.test_obj.assertEqual(expected_element_clicked, element_clicked)
    self.test_obj.assertEqual(self.session_info, session_info)
    self.test_obj.assertEqual(self.screen_info, screen_info)
    return fase_model.Response(screen=self.element_clicked_screen,
                               elements_update=self.element_clicked_elements_update,
                               session_info=self.element_clicked_session_info,
                               screen_info=self.element_clicked_screen_info)


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
    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    client = fase_client.FaseClient(http_client=http_client, ui=ui)

    service = hello_world.HelloWorldService()
    screen = service.OnStart()

    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_service_calls)
    self.assertEqual(1, ui.draw_screen_calls)

  def testGetScreen(self):
    service = hello_world.HelloWorldService()

    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    session_info_tmp = tempfile.NamedTemporaryFile()
    fase_client.SaveSessionInfoIfNeeded(session_info_tmp.name, fase_model.SessionInfo(service.GetSessionId()))
    client = fase_client.FaseClient(http_client=http_client, ui=ui, session_info_filepath=session_info_tmp.name)

    screen = service.OnStart()
    
    http_client.service = service
    http_client.screen = screen
    http_client.session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.screen_info = fase_model.ScreenInfo(screen.GetScreenId())
    ui.expected_screen = screen
    client.Run()
    self.assertEqual(1, http_client.get_screen_calls)
    self.assertEqual(1, ui.draw_screen_calls)

  def testScreenUpdateSendElementsUpdate(self):
    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    client = fase_client.FaseClient(http_client=http_client, ui=ui)

    service = hello_world.HelloWorldService()
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
    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    client = fase_client.FaseClient(http_client=http_client, ui=ui)

    service = hello_world.HelloWorldService()
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
    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    client = fase_client.FaseClient(http_client=http_client, ui=ui)

    service = hello_world.HelloWorldService()
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
    service, screen = screen.GetElement(id_='next_button_id').FaseOnClick(service, screen)
    http_client.screen = screen
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    ui.expected_screen = screen
    client.ScreenUpdate()
    self.assertEqual(2, ui.draw_screen_calls)
    self.assertEqual(0, ui.element_updated_received_calls)

  def testElementClickedElementsUpdateReceived(self):
    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    client = fase_client.FaseClient(http_client=http_client, ui=ui)

    service = hello_world.HelloWorldService()
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
    service, element_clicked_screen = screen.GetElement(id_='next_button_id').FaseOnClick(service, screen)
    http_client.expected_id_list = ['next_button_id']
    http_client.element_clicked_screen = element_clicked_screen
    http_client.element_clicked_session_info = fase_model.SessionInfo(service.GetSessionId())
    http_client.element_clicked_screen_info = fase_model.ScreenInfo(element_clicked_screen.GetScreenId())
    ui.expected_id_list = ['text_name_id']
    ui.expected_value = 'Hanry Ford'
    ui.expected_screen = element_clicked_screen
    client.ElementClicked(id_list=['next_button_id'])
    self.assertEqual(1, http_client.element_clicked_calls)
    self.assertEqual(2, ui.draw_screen_calls)
    self.assertEqual(1, ui.element_updated_received_calls)

  def testElementClickedScreenReceived(self):
    http_client = MockFaseHTTPClient(self)
    ui = MockFaseUI(self)
    client = fase_client.FaseClient(http_client=http_client, ui=ui)

    service = hello_world.HelloWorldService()
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
    service, screen = screen.GetElement(id_='next_button_id').FaseOnClick(service, screen)
    http_client.screen = screen
    client.ScreenUpdate()
    time.sleep(0.1)
    self.assertEqual(1, http_client.screen_update_calls)

    ui.expected_screen = screen
    client.ElementClicked(id_list=['next_button_id'])
    self.assertEqual(2, ui.draw_screen_calls)
    self.assertEqual(0, ui.element_updated_received_calls)


if __name__ == '__main__':
    unittest.main()
