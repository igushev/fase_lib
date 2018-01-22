import logging
import requests

import fase
import fase_model
import json_util


class FaseHTTPClient(object):

  def __init__(self, server_url):
    self.server_url = server_url

  def AssertStatus(self, http_response):
    if http_response.status_code != requests.codes.ok:
      logging.error(http_response.text)
      http_response.raise_for_status()

  def GetService(self, device):
    url = self.server_url + '/getservice'
    device_simple = device.ToSimple()
    http_response = requests.post(url, json=device_simple)
    self.AssertStatus(http_response)
    response_simple = http_response.json()
    response = fase_model.Response.FromSimple(response_simple)
    return response

  def GetScreen(self, device, session_info):
    url = self.server_url + '/getscreen'
    headers = {'session-id': session_info.session_id}
    device_simple = device.ToSimple()
    http_response = requests.post(url, headers=headers, json=device_simple)
    self.AssertStatus(http_response)
    response_simple = http_response.json()
    response = fase_model.Response.FromSimple(response_simple)
    return response

  def ScreenUpdate(self, screen_update, session_info, screen_info):
    url = self.server_url + '/screenupdate'
    headers = {'session-id': session_info.session_id, 'screen-id': screen_info.screen_id}
    screen_update_simple = screen_update.ToSimple()
    http_response = requests.post(url, headers=headers, json=screen_update_simple)
    self.AssertStatus(http_response)
    response_simple = http_response.json()
    response = fase_model.Response.FromSimple(response_simple)
    return response
    
  def ElementClicked(self, element_clicked, session_info, screen_info):
    url = self.server_url + '/elementclicked'
    headers = {'session-id': session_info.session_id, 'screen-id': screen_info.screen_id}
    element_clicked_simple = element_clicked.ToSimple()
    http_response = requests.post(url, headers=headers, json=element_clicked_simple)
    self.AssertStatus(http_response)
    response_simple = http_response.json()
    response = fase_model.Response.FromSimple(response_simple)
    return response
