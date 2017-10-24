import fase


class HelloWorldService(fase.Service):
  
  
  def OnStart(self):
    screen = fase.Screen()
    screen.AddText('text_name_id', hint='Enter Name')
    screen.AddButton('next_button_id',
                     text='Next', on_click=HelloWorldService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetElement('text_name_id').GetText()
    label = 'Hello, %s!' % name
    screen = fase.Screen()
    screen.AddLabel('hello_label_id', label=label)
    screen.AddButton('reset_button_id',
                     text='Reset', on_click=HelloWorldService.OnResetButton)
    return screen
    
  def OnResetButton(self, screen, element):
    # Ignore previous screen and element.
    return self.OnStart()
