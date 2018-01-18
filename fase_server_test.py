import unittest

import fase_database
import fase_model
import fase_server
import fase
import hello_world


class FaseTest(unittest.TestCase):

  def setUp(self):
    super(FaseTest, self).setUp()
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_prog_list=[], user_list=[]), overwrite=True)
    fase_server.FaseServer.Set(fase_server.FaseServer(), overwrite=True)

  def testSendInternalCommand(self):
    command = fase_model.Command(fase_server.CREATE_DB_COMMAND)
    status = fase_server.FaseServer.Get().SendInternalCommand(command)
    self.assertEqual(fase_server.TABLES_CREATED, status.message)

    command = fase_model.Command(fase_server.DELETE_DB_COMMAND)
    status = fase_server.FaseServer.Get().SendInternalCommand(command)
    self.assertEqual(fase_server.TABLES_DELETED, status.message)

  def testSendInternalCommandError(self):
    command = fase_model.Command('FAKE_COMMAND')
    self.assertRaises(fase_server.BadRequestException, fase_server.FaseServer.Get().SendInternalCommand, command)

  def testSendServiceCommand(self):
    command = fase_model.Command('ServiceName')
    status = fase_server.FaseServer.Get().SendServiceCommand(command)
    self.assertEqual('HelloWorld', status.message)

  def testHelloWorld(self):
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server.FaseServer.Get().GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = fase.Screen(service)
    expected_screen.AddText(id_='text_name_id', hint='Enter Name')
    expected_screen.AddButton(id_='next_button_id', text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server.FaseServer.Get().GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response = fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    expected_screen.GetElement(id_='text_name_id').Update('Hanry Ford')
    self.assertEqual(expected_screen, response.screen)
    response = fase_server.FaseServer.Get().GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(id_list=['next_button_id'])
    response = fase_server.FaseServer.Get().ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = fase.Screen(service)
    expected_screen.AddLabel(id_='hello_label_id', label='Hello, Hanry Ford!')
    expected_screen.AddButton(id_='reset_button_id',text='Reset', on_click=hello_world.HelloWorldService.OnResetButton)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server.FaseServer.Get().GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(id_list=['reset_button_id'])
    response = fase_server.FaseServer.Get().ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = fase.Screen(service)
    expected_screen.AddText(id_='text_name_id', hint='Enter Name')
    expected_screen.AddButton(id_='next_button_id', text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server.FaseServer.Get().GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

  def testHelloWorldElementClickedWithScreenUpdate(self):
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server.FaseServer.Get().GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    expected_screen = fase.Screen(service)
    expected_screen.AddText(id_='text_name_id', hint='Enter Name')
    expected_screen.AddButton(id_='next_button_id', text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server.FaseServer.Get().GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    element_clicked = fase_model.ElementClicked(screen_update=screen_update, id_list=['next_button_id'])
    response = fase_server.FaseServer.Get().ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = fase.Screen(service)
    expected_screen.AddLabel(id_='hello_label_id', label='Hello, Hanry Ford!')
    expected_screen.AddButton(id_='reset_button_id',text='Reset', on_click=hello_world.HelloWorldService.OnResetButton)
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server.FaseServer.Get().GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

  def testElementClickedScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server.FaseServer.Get().GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    
    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response_entered_text = fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    screen_info_entered_text = response_entered_text.screen_info

    element_clicked = fase_model.ElementClicked(id_list=['next_button_id'])
    response_clicked_next = fase_server.FaseServer.Get().ElementClicked(
        element_clicked, session_info, screen_info_entered_text)
    screen_info_clicked_next = response_clicked_next.screen_info
    screen_clicked_next = response_clicked_next.screen

    response_click_again = fase_server.FaseServer.Get().ElementClicked(
        element_clicked, session_info, screen_info_entered_text)
    self.assertEqual(screen_info_clicked_next, response_click_again.screen_info)
    self.assertEqual(screen_clicked_next, response_click_again.screen)

  def testScreenUpdateScreenInfoObsolete(self):
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server.FaseServer.Get().GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    
    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response_entered_text = fase_server.FaseServer.Get().ScreenUpdate(screen_update, session_info, screen_info)
    screen_info_entered_text = response_entered_text.screen_info

    element_clicked = fase_model.ElementClicked(id_list=['next_button_id'])
    response_clicked_next = fase_server.FaseServer.Get().ElementClicked(
        element_clicked, session_info, screen_info_entered_text)
    screen_info_clicked_next = response_clicked_next.screen_info
    screen_clicked_next = response_clicked_next.screen

    response_enter_text_again = fase_server.FaseServer.Get().ScreenUpdate(
        screen_update, session_info, screen_info_entered_text)
    self.assertEqual(screen_info_clicked_next, response_enter_text_again.screen_info)
    self.assertEqual(screen_clicked_next, response_enter_text_again.screen)


if __name__ == '__main__':
    unittest.main()
