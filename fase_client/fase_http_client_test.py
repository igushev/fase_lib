import unittest
import requests

from fase_lib import fase
from fase_lib.fase_model import fase_model

import fase_http_client


MOCK_URL = 'mock.url'


class MockRequests(object):

  def __init__(self, test_obj):
    self.test_obj = test_obj
    self.expected_url = None
    self.expected_headers = None
    self.expected_json = None
    self.response = None

  class codes:
    ok = object()

  def post(self, url, headers=None, json=None):
    self.test_obj.assertEqual(self.expected_url, url)
    self.test_obj.assertEqual(self.expected_headers, headers)
    self.test_obj.assertEqual(self.expected_json, json)
    return MockHTTPResponse(MockRequests.codes.ok, self.response.ToSimple())


class MockHTTPResponse(object):

  def __init__(self, status_code, json):
    self.status_code = status_code
    self.json_obj = json
    
  def json(self):
    return self.json_obj


class FaseHTTPClientTest(unittest.TestCase):

  def testGetService(self):
    self.requests_bkp = fase_http_client.requests 
    fase_http_client.requests = MockRequests(self) 
    
    http_client = fase_http_client.FaseHTTPClient(MOCK_URL)
    device = fase_model.Device(device_type='MockType', device_id='MockDeviceID')
    response = fase_model.Response()
    fase_http_client.requests.expected_url = MOCK_URL + '/getservice'
    fase_http_client.requests.expected_json = device.ToSimple()
    fase_http_client.requests.response = response
    actual_response = http_client.GetService(device)
    self.assertEqual(response, actual_response)
  
    fase_http_client.requests = self.requests_bkp

  def testGetScreen(self):
    self.requests_bkp = fase_http_client.requests 
    fase_http_client.requests = MockRequests(self) 
    
    http_client = fase_http_client.FaseHTTPClient(MOCK_URL)
    device = fase_model.Device(device_type='MockType', device_id='MockDeviceID')
    session_info = fase_model.SessionInfo(session_id='MockSessionId')
    response = fase_model.Response()
    fase_http_client.requests.expected_url = MOCK_URL + '/getscreen'
    fase_http_client.requests.expected_headers = {'session-id': session_info.session_id}
    fase_http_client.requests.expected_json = device.ToSimple()
    fase_http_client.requests.response = response
    actual_response = http_client.GetScreen(device, session_info)
    self.assertEqual(response, actual_response)
  
    fase_http_client.requests = self.requests_bkp

  def testScreenUpdateAndElementCallback(self):
    self.requests_bkp = fase_http_client.requests 
    fase_http_client.requests = MockRequests(self) 
    
    http_client = fase_http_client.FaseHTTPClient(MOCK_URL)
    device = fase_model.Device(device_type='MockType', device_id='MockDeviceID')
    session_info = fase_model.SessionInfo(session_id='MockSessionId')
    screen_info = fase_model.ScreenInfo(screen_id='MockScreenId')
    response = fase_model.Response()
    for url_method, http_client_method in [('/screenupdate', http_client.ScreenUpdate),
                                           ('/elementcallback', http_client.ElementCallback)]:
      fase_http_client.requests.expected_url = MOCK_URL + url_method
      fase_http_client.requests.expected_headers = {
          'session-id': session_info.session_id, 'screen-id': screen_info.screen_id}
      fase_http_client.requests.expected_json = device.ToSimple()
      fase_http_client.requests.response = response
      actual_response = http_client_method(device, session_info, screen_info)
      self.assertEqual(response, actual_response)
  
    fase_http_client.requests = self.requests_bkp


if __name__ == '__main__':
    unittest.main()
