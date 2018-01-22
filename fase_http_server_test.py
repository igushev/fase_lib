import json
import unittest

import fase
import fase_database
import fase_model
import fase_server
import fase_http_server
import hello_world

STATUS_OK = '200 OK'
STATUS_BAD_REQUEST = '400 BAD REQUEST'


class ApplicationTest(unittest.TestCase):

  def setUp(self):
    super(ApplicationTest, self).setUp()
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_prog_list=[], user_list=[]), overwrite=True)
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
    response = fase_model.Response.FromSimple(json.loads(result.data.decode('utf-8')))
    return response

  def _GetScreen(self, device, session_info):
    result = self.test_application.post(
        '/getscreen',
        headers={'session_id': session_info.session_id},
        data=json.dumps(device.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response = fase_model.Response.FromSimple(json.loads(result.data.decode('utf-8')))
    return response

  def _ScreenUpdate(self, screen_update, session_info, screen_info):
    result = self.test_application.post(
        '/screenupdate',
        headers={'session_id': session_info.session_id, 'screen_id': screen_info.screen_id},
        data=json.dumps(screen_update.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response = fase_model.Response.FromSimple(json.loads(result.data.decode('utf-8')))
    return response

  def _ElementClicked(self, element_clicked, session_info, screen_info):
    result = self.test_application.post(
        '/elementclicked',
        headers={'session_id': session_info.session_id, 'screen_id': screen_info.screen_id},
        data=json.dumps(element_clicked.ToSimple()))
    self.AssertResultStatus(STATUS_OK, result)
    response = fase_model.Response.FromSimple(json.loads(result.data.decode('utf-8')))
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
    screen.AddButton(id_='next_button_id', text='Next', on_click=fase.MockFunction)
    return screen

  @staticmethod
  def _GetGreetingScreen(service, name):
    screen = fase.Screen(service)
    screen.AddLabel(id_='hello_label_id', label='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id',text='Reset', on_click=fase.MockFunction)
    return screen

  def testHelloWorld(self):
    device = fase_model.Device('MockType', 'MockToken')
    response = self._GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = ApplicationTest._GetEnterNameScreen(service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)
    
    elements_update=fase_model.ElementsUpdate([['text_name_id']], ['Hanry Ford'])
    screen_update = fase_model.ScreenUpdate(elements_update=elements_update, device=device)
    response = self._ScreenUpdate(screen_update, session_info, screen_info)
    expected_screen = ApplicationTest._GetEnterNameScreen(service, name='Hanry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertIsNone(response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(id_list=['next_button_id'], device=device)
    response = self._ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = ApplicationTest._GetGreetingScreen(service, name='Hanry Ford')
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(id_list=['reset_button_id'], device=device)
    response = self._ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = ApplicationTest._GetEnterNameScreen(service)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = self._GetScreen(device, session_info)
    self.assertEqual(expected_screen, response.screen)


if __name__ == '__main__':
    unittest.main()
