import fase


class HelloWorldService(fase.Service):

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddText(id_='text_name_id', hint='Enter Name')
    screen.AddButton(id_='next_button_id', text='Next', on_click=HelloWorldService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetText(id_='text_name_id').GetText()
    screen = fase.Screen(self)
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id', text='Reset', on_click=HelloWorldService.OnResetButton)
    return screen

  def OnResetButton(self, screen, element):
    # Ignore previous screen and element.
    return self.OnStart()
