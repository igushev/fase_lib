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
            service_list=[], screen_list=[], user_list=[]), overwrite=True)
    fase_server_ = fase_server.FaseServer()
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server_.GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    expected_screen = fase.Screen()
    expected_screen.AddText(id_='text_name_id', hint='Enter Name')
    expected_screen.AddButton(id_='next_button_id', text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._session_id = session_info.session_id
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)
    
    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response = fase_server_.ScreenUpdate(screen_update, session_info, screen_info)
    expected_screen.GetElement(id_='text_name_id').Update('Hanry Ford')
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(['next_button_id'])
    response = fase_server_.ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = fase.Screen()
    expected_screen.AddLabel(id_='hello_label_id', label='Hello, Hanry Ford!')
    expected_screen.AddButton(id_='reset_button_id',text='Reset', on_click=hello_world.HelloWorldService.OnResetButton)
    expected_screen._session_id = session_info.session_id
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

    element_clicked = fase_model.ElementClicked(['reset_button_id'])
    response = fase_server_.ElementClicked(element_clicked, session_info, screen_info)
    screen_info = response.screen_info
    expected_screen = fase.Screen()
    expected_screen.AddText(id_='text_name_id', hint='Enter Name')
    expected_screen.AddButton(id_='next_button_id', text='Next', on_click=hello_world.HelloWorldService.OnNextButton)
    expected_screen._session_id = session_info.session_id
    expected_screen._screen_id = screen_info.screen_id
    self.assertEqual(expected_screen, response.screen)
    response = fase_server_.GetScreen(session_info)
    self.assertEqual(expected_screen, response.screen)

  def testElementClickedScreenInfoObsolete(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_list=[], user_list=[]), overwrite=True)
    fase_server_ = fase_server.FaseServer()
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server_.GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    
    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response_entered_text = fase_server_.ScreenUpdate(screen_update, session_info, screen_info)
    screen_info_entered_text = response_entered_text.screen_info

    element_clicked = fase_model.ElementClicked(['next_button_id'])
    response_clicked_next = fase_server_.ElementClicked(element_clicked, session_info, screen_info_entered_text)
    screen_info_clicked_next = response_clicked_next.screen_info
    screen_clicked_next = response_clicked_next.screen

    response_click_again = fase_server_.ElementClicked(element_clicked, session_info, screen_info_entered_text)
    self.assertEqual(screen_info_clicked_next, response_click_again.screen_info)
    self.assertEqual(screen_clicked_next, response_click_again.screen)

  def testScreenUpdateScreenInfoObsolete(self):
    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_list=[], screen_list=[], user_list=[]), overwrite=True)
    fase_server_ = fase_server.FaseServer()
    device = fase_model.Device('MockType', 'MockToken')
    response = fase_server_.GetService(device)
    session_info = response.session_info
    screen_info = response.screen_info
    
    screen_update = fase_model.ScreenUpdate([['text_name_id']], ['Hanry Ford'])
    response_entered_text = fase_server_.ScreenUpdate(screen_update, session_info, screen_info)
    screen_info_entered_text = response_entered_text.screen_info

    element_clicked = fase_model.ElementClicked(['next_button_id'])
    response_clicked_next = fase_server_.ElementClicked(element_clicked, session_info, screen_info_entered_text)
    screen_info_clicked_next = response_clicked_next.screen_info
    screen_clicked_next = response_clicked_next.screen

    response_enter_text_again = fase_server_.ScreenUpdate(screen_update, session_info, screen_info_entered_text)
    self.assertEqual(screen_info_clicked_next, response_enter_text_again.screen_info)
    self.assertEqual(screen_clicked_next, response_enter_text_again.screen)


if __name__ == '__main__':
    unittest.main()
