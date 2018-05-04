import json
import unittest

from base_util import json_util

from fase import fase
from fase_model import fase_model

import fase_database
import fase_http_server
import fase_server


STATUS_OK = '200 OK'
STATUS_BAD_REQUEST = '400 BAD REQUEST'


def CleanSimple(simple):
  if isinstance(simple, list):
    return [CleanSimple(nested_simple) for nested_simple in simple]
  elif isinstance(simple, dict):
    clean_simple = {}
    for nested_key, nested_simple in simple.items():
      if nested_key in [fase.ON_CLICK_METHOD, fase.ON_PICK_METHOD, fase.ON_REFRESH_METHOD, fase.ON_MORE_METHOD]:
        clean_simple[nested_key] = (
            json_util.JSONFunction().ToSimple(fase.FunctionPlaceholder) if nested_simple is not None else None)
      else:
        clean_simple[nested_key] = CleanSimple(nested_simple)
    return clean_simple
  else:
    return simple


class ApplicationTestService(fase.Service):

  @staticmethod
  def ServiceCommand(command):
    if command.command == 'ServiceName':
      return 'HelloWorld'
    else:
      raise AssertionError('Wrong ServiceCommand') 

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddText(id_='text_name_id', hint='Enter Name')
    screen.AddButton(id_='next_button_id', text='Next', on_click=ApplicationTestService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetText(id_='text_name_id').GetText()
    screen = fase.Screen(self)
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id', text='Reset', on_click=ApplicationTestService.OnResetButton)
    return screen
    
  def OnResetButton(self, screen, element):
    # Ignore previous screen and element.
    return self.OnStart()


fase.Service.RegisterService(ApplicationTestService)


class ApplicationTest(unittest.TestCase):

  def setUp(self):
    super(ApplicationTest, self).setUp()
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_prog_list=[], screen_prog_list=[], user_list=[]), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)
    self.test_application = fase_http_server.application.test_client()

  def AssertResultStatus(self, expected_status, result):
    if expected_status != result.status:
      print(result.data.decode('utf-8'))
      self.fail()

  def _SendInternalCommand(self, command):
    result = self.test_application.post(
        '/sendinternalcommand',
        data=json.dumps(command.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    status = fase_model.Status.FromSimple(json.loads(result.data.decode('utf-8')))
    return status

  def _SendInternalCommandAndAssertFails(self, command, bad_request):
    result = self.test_application.post(
        '/sendinternalcommand',
        data=json.dumps(command.ToSimple()))
    self.AssertResultStatus(STATUS_BAD_REQUEST, result)
    self.assertEqual(bad_request, fase_model.BadRequest.FromSimple(json.loads(result.data.decode('utf-8'))))

  def _SendServiceCommand(self, command):
    result = self.test_application.post(
        '/sendservicecommand',
        data=json.dumps(command.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    status = fase_model.Status.FromSimple(json.loads(result.data.decode('utf-8')))
    return status

  def _GetService(self, device):
    result = self.test_application.post(
        '/getservice',
        data=json.dumps(device.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response_simple = json.loads(result.data.decode('utf-8'))
    response_simple = CleanSimple(response_simple)
    response = fase_model.Response.FromSimple(response_simple)
    return response

  def _GetScreen(self, device, session_info):
    result = self.test_application.post(
        '/getscreen',
        headers={'session_id': session_info.session_id},
        data=json.dumps(device.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response_simple = json.loads(result.data.decode('utf-8'))
    response_simple = CleanSimple(response_simple)
    response = fase_model.Response.FromSimple(response_simple)
    return response

  def _ScreenUpdate(self, screen_update, session_info, screen_info):
    result = self.test_application.post(
        '/screenupdate',
        headers={'session_id': session_info.session_id, 'screen_id': screen_info.screen_id},
        data=json.dumps(screen_update.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response_simple = json.loads(result.data.decode('utf-8'))
    response_simple = CleanSimple(response_simple)
    response = fase_model.Response.FromSimple(response_simple)
    return response

  def _ElementCallback(self, element_callback, session_info, screen_info):
    result = self.test_application.post(
        '/elementcallback',
        headers={'session_id': session_info.session_id, 'screen_id': screen_info.screen_id},
        data=json.dumps(element_callback.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response_simple = json.loads(result.data.decode('utf-8'))
    response_simple = CleanSimple(response_simple)
    response = fase_model.Response.FromSimple(response_simple)
    return response

  def testSendInternalCommand(self):
    command = fase_model.Command(fase_server.CREATE_DB_COMMAND)
    status = self._SendInternalCommand(command)
    self.assertEqual(fase_server.TABLES_CREATED, status.message)

    command = fase_model.Command(fase_server.DELETE_DB_COMMAND)
    status = self._SendInternalCommand(command)
    self.assertEqual(fase_server.TABLES_DELETED, status.message)

  def testSendInternalCommandError(self):
    command = fase_model.Command('FAKE_COMMAND')
    self._SendInternalCommandAndAssertFails(command, fase_server.WRONG_COMMAND)

  def testSendServiceCommand(self):
    command = fase_model.Command('ServiceName')
    status = self._SendServiceCommand(command)
    self.assertEqual('HelloWorld', status.message)

  @staticmethod
  def _GetEnterNameScreen(service, name=None):
    screen = fase.Screen(service)
    screen.AddText(id_='text_name_id', hint='Enter Name', text=name)
    screen.AddButton(id_='next_button_id', text='Next', on_click=fase.FunctionPlaceholder)
    return screen

  @staticmethod
  def _GetGreetingScreen(service, name):
    screen = fase.Screen(service)
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id',text='Reset', on_click=fase.FunctionPlaceholder)
    return screen

  def testService(self):
    device = fase.Device('MockType', 'MockToken')
    response = self._GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    expected_screen = ApplicationTest._GetEnterNameScreen(service_prog.service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)
    
    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Hanry Ford'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response = self._ScreenUpdate(screen_update, session_info, screen_info)
    expected_screen = ApplicationTest._GetEnterNameScreen(service_prog.service, name='Hanry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertIsNone(response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)

    element_callback = (
        fase_model.ElementCallback(id_list=['next_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response = self._ElementCallback(element_callback, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = ApplicationTest._GetGreetingScreen(service_prog.service, name='Hanry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)

    element_callback = (
        fase_model.ElementCallback(id_list=['reset_button_id'], method=fase.ON_CLICK_METHOD, device=device))
    response = self._ElementCallback(element_callback, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = ApplicationTest._GetEnterNameScreen(service_prog.service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)


if __name__ == '__main__':
    unittest.main()
