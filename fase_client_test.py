import unittest
import tempfile

import hello_world
import fase_client
import fase_model


class MockFaseHTTPClient(object):
  pass


class MockFaseUI(object):

  def SetClient(self, client):
    self.client = client

  def Run(self):
    pass


class FaseServerTest(unittest.TestCase):
  
  def testGetService(self):
    expected_service = hello_world.HelloWorldService()
    expected_screen = expected_service.OnStart()
    
    def MockGetService(device):
      self.assertEqual('Python', device.device_type)
      return fase_model.Response(screen=expected_screen,
                                 session_info=fase_model.SessionInfo(expected_service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(expected_screen.GetScreenId()))
    http_client = MockFaseHTTPClient()
    http_client.GetService = MockGetService

    def MockDrawScreen(screen):
      self.assertEqual(expected_screen, screen)

    ui = MockFaseUI()
    ui.DrawScreen = MockDrawScreen

    client = fase_client.FaseClient(http_client=http_client, ui=ui)
    client.Run()

  def testGetScreen(self):
    expected_service = hello_world.HelloWorldService()
    expected_screen = expected_service.OnStart()
    expected_session_info = fase_model.SessionInfo(expected_service.GetSessionId())
    
    def MockGetScreen(device, session_info):
      self.assertEqual('Python', device.device_type)
      self.assertEqual(expected_session_info, session_info)
      return fase_model.Response(screen=expected_screen,
                                 session_info=expected_session_info,
                                 screen_info=fase_model.ScreenInfo(expected_screen.GetScreenId()))
    http_client = MockFaseHTTPClient()
    http_client.GetScreen = MockGetScreen

    def MockDrawScreen(screen):
      self.assertEqual(expected_screen, screen)

    ui = MockFaseUI()
    ui.DrawScreen = MockDrawScreen

    session_info_tmp = tempfile.NamedTemporaryFile()
    fase_client.SaveSessionInfoIfNeeded(session_info_tmp.name, expected_session_info)
    client = fase_client.FaseClient(http_client=http_client, ui=ui, session_info_filepath=session_info_tmp.name)
    client.Run()


if __name__ == '__main__':
    unittest.main()
