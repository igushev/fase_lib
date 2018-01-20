import os
import pickle
import uuid

import fase
import fase_model
import fase_sign_in


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
    self.device = fase_model.Device('Python', str(uuid.uuid4()))
    self.screen = None
    self.session_info = LoadSessionInfoIfExists(self.session_info_filepath)
    self.screen_info = None

  def Run(self):
    if self.session_info is None:
      response = self.http_client.GetService(self.device)
    else:
      response = self.http_client.GetScreen(self.device, self.session_info)
    self.ProcessResponse(response)
    self.ui.Run()

  @staticmethod
  def _ElementsUpdateToDict(elements_update):
    return {tuple(id_list): value for id_list, value in zip(elements_update.id_list_list, elements_update.value_list)}

  @staticmethod
  def _DictToElementsUpdate(id_list_to_value):
    if not id_list_to_value:
      return None
    id_list_list = []
    value_list = []
    for id_list, value in id_list_to_value.items():
      id_list_list.append(list(id_list))
      value_list.append(value)
    return fase_model.ElementsUpdate(id_list_list=id_list_list, value_list=value_list)

  def ScreenUpdate(self, id_list_to_value):
    elements_update = FaseClient._DictToElementsUpdate(id_list_to_value)
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=self.device)
    response = self.http_client.ScreenUpdate(screen_update, self.session_info, self.screen_info)
    self.ProcessResponse(response)

  def ElementClicked(self, id_list, id_list_to_value):
    elements_update = FaseClient._DictToElementsUpdate(id_list_to_value)
    element_clicked = fase_model.ElementClicked(elements_update=elements_update, id_list=id_list, device=self.device)
    response = self.http_client.ElementClicked(element_clicked, self.session_info, self.screen_info)
    self.ProcessResponse(response)

  def ProcessResponse(self, response):
    while response.screen is not None and response.screen.HasElement(fase.POPUP_ID):
      popup = response.screen.PopElement(fase.POPUP_ID)
      id_list = self.ui.ShowPopup(popup)
      element_clicked = fase_model.ElementClicked(id_list=id_list)
      response = self.http_client.ElementClicked(element_clicked, response.session_info, response.screen_info)
    self.session_info = response.session_info
    self.screen_info = response.screen_info
    SaveSessionInfoIfNeeded(self.session_info_filepath, response.session_info)
    if response.screen:
      self.ui.DrawScreen(response.screen)
    elif response.elements_update:
      self.ui.ElementsUpdateReceived(FaseClient._ElementsUpdateToDict(response.elements_update))
    self.ui.ResetValues()
