import uuid

import fase
import fase_model
import fase_sign_in


class FaseClient(object):
  
  def __init__(self, http_client, ui):
    self.http_client = http_client
    self.ui = ui
    self.ui.SetClient(self)
    self.screen = None
    self.session_info = None
    self.screen_info = None

  def Run(self):
    response = self.http_client.GetService(fase_model.Device('Python', str(uuid.getnode())))
    self.ProcessResponse(response)
    self.ui.Run()

  def ElementClicked(self, id_list, id_list_to_value):
    if len(id_list_to_value):
      id_list_list = []
      value_list = []
      for id_list_update, value in id_list_to_value.items():
        id_list_list.append(list(id_list_update))
        value_list.append(value)
      screen_update = fase_model.ScreenUpdate(id_list_list=id_list_list, value_list=value_list)
      self.http_client.ScreenUpdate(screen_update, self.session_info, self.screen_info)
    element_clicked = fase_model.ElementClicked(id_list)
    response = self.http_client.ElementClicked(element_clicked, self.session_info, self.screen_info)
    self.ProcessResponse(response)
    self.ui.ResetValues()

  def ProcessResponse(self, response):
    while response.screen.HasElement(fase.POPUP_ID):
      popup = response.screen.PopElement(fase.POPUP_ID)
      id_list = self.ui.ShowPopup(popup)
      element_clicked = fase_model.ElementClicked(id_list)
      response = self.http_client.ElementClicked(element_clicked, response.session_info, response.screen_info)
    self.session_info = response.session_info
    self.screen_info = response.screen_info
    self.ui.DrawScreen(response.screen)
