import unittest

import fase_database
import fase_model
import fase_server
import fase
import hello_world


class FaseTest(unittest.TestCase):

  def testHelloWorld(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_list=[], user_list=[]))
    fase_server_ = fase_server.FaseServer()
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server_.GetService(device)
    session_info = response.session_info
    expected_screen = fase.Screen()
    expected_screen.AddText('text_name_id', hint='Enter Name')
    expected_screen.AddButton(
        'next_button_id',
        text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._session_id = session_info.session_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)
    
    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response = fase_server_.ScreenUpdate(screen_update, session_info)
    expected_screen.GetElement('text_name_id').Update('Hanry Ford')
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(['next_button_id'])
    response = fase_server_.ElementClicked(element_clicked, session_info)
    expected_screen = fase.Screen()
    expected_screen.AddLabel('hello_label_id', label='Hello, Hanry Ford!')
    expected_screen.AddButton(
        'reset_button_id',
        text='Reset', on_click=hello_world.HelloWorldService.OnResetButton)
    expected_screen._session_id = session_info.session_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(['reset_button_id'])
    response = fase_server_.ElementClicked(element_clicked, session_info)
    expected_screen = fase.Screen()
    expected_screen.AddText('text_name_id', hint='Enter Name')
    expected_screen.AddButton(
        'next_button_id',
        text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._session_id = session_info.session_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)


if __name__ == '__main__':
    unittest.main()
