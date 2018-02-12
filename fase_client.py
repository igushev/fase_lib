import os
import pickle
import uuid
import queue
import threading

import fase
import fase_model
import fase_sign_in

COUNTRY_CODE = 'US'
DEVICE_TYPE = 'Python'


def LoadSessionInfoIfExists(session_info_filepath):
  if session_info_filepath is None or not os.path.exists(session_info_filepath):
    return None
  with open(session_info_filepath, 'rb') as session_info_file:
    return pickle.load(session_info_file)


def SaveSessionInfoIfNeeded(session_info_filepath, session_info):
  if session_info_filepath is None:
    return
  with open(session_info_filepath, 'wb') as session_info_file:
    return pickle.dump(session_info, session_info_file)


class FaseClient(object):
  
  def __init__(self, http_client, ui, session_info_filepath=None):
    self.http_client = http_client
    self.ui = ui
    self.ui.SetClient(self)
    self.session_info_filepath = session_info_filepath
    self.device = fase_model.Device(DEVICE_TYPE, str(uuid.uuid4()))
    self.screen = None
    self.elements_update = None
    self.session_info = LoadSessionInfoIfExists(self.session_info_filepath)
    self.screen_info = None

    self.id_list_to_value = dict()
    self.id_list_to_value_lock = threading.Lock()

    self.screen_lock = threading.Lock()
    self.screen_update_condition = threading.Condition(self.screen_lock)
    self.screen_update_response_queue = queue.Queue(maxsize=1)
    self.screen_update_thread = threading.Thread(target=self._ScreenUpdateThread)
    self.screen_update_thread.daemon = True
    self.screen_update_thread.start()

  def Run(self):
    if self.session_info is None:
      response = self.http_client.GetService(self.device)
    else:
      response = self.http_client.GetScreen(self.device, self.session_info)
    self.ProcessResponse(response)
    self.ui.Run()

  def ElementUpdated(self, id_list, value):
    with self.id_list_to_value_lock:
      self.id_list_to_value[tuple(id_list)] = value

  def _ScreenUpdateThread(self):
    with self.screen_lock:
      while True:
        self.screen_update_condition.wait()
        with self.id_list_to_value_lock:
          elements_update = fase_model.DictToElementsUpdate(self.id_list_to_value)
          self._ResetValues()
        screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=self.device)
        response = self.http_client.ScreenUpdate(screen_update, self.session_info, self.screen_info)
        self.screen_update_response_queue.put(response)

  def ScreenUpdate(self):
    if not self.screen_lock.acquire(blocking=False):
      return
    if not self.screen_update_response_queue.empty():
      response = self.screen_update_response_queue.get(block=False)
      self.ProcessResponse(response)
    self.screen_update_condition.notify()
    self.screen_lock.release()

  def _GetElementCallback(self, elements_update, id_list):
    element = fase_model.GetScreenElement(self.screen, id_list)
    locale = fase.Locale(country_code=COUNTRY_CODE) if element.GetRequestLocale() else None
    return fase_model.ElementCallback(
        elements_update=elements_update, id_list=id_list, device=self.device, locale=locale)

  def ElementCallback(self, id_list):
    with self.screen_lock:
      if not self.screen_update_response_queue.empty():
        response = self.screen_update_response_queue.get(block=False)
        if self.ProcessResponse(response):  # If screen has been updated, the click is obsolete.
          return
      with self.id_list_to_value_lock:
        elements_update = fase_model.DictToElementsUpdate(self.id_list_to_value)
        self._ResetValues()
      element_callback = self._GetElementCallback(elements_update=elements_update, id_list=id_list)
      response = self.http_client.ElementCallback(element_callback, self.session_info, self.screen_info)
      self.ProcessResponse(response)

  def ProcessResponse(self, response):
    while response.screen is not None and response.screen.HasElement(fase.ALERT_ID):
      alert = response.screen.PopElement(fase.ALERT_ID)
      id_list = self.ui.ShowAlert(alert)
      element_callback = fase_model.ElementCallback(id_list=id_list, device=self.device)
      response = self.http_client.ElementCallback(element_callback, response.session_info, response.screen_info)
    self.session_info = response.session_info
    self.screen_info = response.screen_info
    SaveSessionInfoIfNeeded(self.session_info_filepath, response.session_info)
    if response.screen:
      self.screen = response.screen
      self.ui.DrawScreen(response.screen)
      return True  # Screen has been updated.
    elif response.elements_update:
      self.elements_update = response.elements_update 
      self._ElementsUpdateReceived(fase_model.ElementsUpdateToDict(response.elements_update))
    return False  # Screen is the same.

  def _ElementsUpdateReceived(self, id_list_to_value):
    for id_list, value in id_list_to_value.items():
      self.ui.ElementUpdatedReceived(list(id_list), value)

  def _ResetValues(self):
    self.id_list_to_value = dict()
