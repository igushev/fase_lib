from fase import fase
from fase import fase_sign_in


class FaseTestService(fase.Service):

  @staticmethod
  def GetServiceId():
    return 'FaseTest'

  @staticmethod
  def ServiceCommand(command):
    if command.command == 'ServiceName':
      return 'FaseTest'
    else:
      raise AssertionError('Wrong ServiceCommand') 

  def OnStart(self):
    screen = fase.Screen(self)
    screen.SetTitle('FaseTest')
    screen.SetScrollable(True)
    self._AddButtons(screen)
    return screen

  def _AddButtons(self, screen):
    navigation = screen.AddNavigation()
    navigation.AddButton(id_='layout_test_button', text='Layout Test', on_click=FaseTestService.OnLayoutTest)
    if self.IfSignedIn():
      navigation.AddButton(id_='sign_out_button', text='Sign Out', on_click=FaseTestService.OnSignOut)
    else:
      navigation.AddButton(id_='sign_in_button', text='Sign In', on_click=FaseTestService.OnSignIn)

  def OnLayoutTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Test layout')
    screen.SetScrollable(True)
    self._AddButtons(screen)
    screen.AddLabel(text='Label Left', align=fase.Label.LEFT)
    screen.AddLabel(text='Label Right', align=fase.Label.RIGHT)
    screen.AddLabel(text='Label Center', align=fase.Label.CENTER)
    screen.AddLabel(text='Text Element Singline')
    screen.AddText(hint='Text Element')
    screen.AddLabel(text='Text Element Multiline')
    screen.AddText(hint='Text Element Multiline', multiline=True)
    screen.AddLabel(text='Switch Element Left')
    screen.AddSwitch(value=True, text='Switch Element', align=fase.Switch.LEFT)
    screen.AddLabel(text='Switch Element Right')
    screen.AddSwitch(value=True, text='Switch Element', align=fase.Switch.RIGHT)
    screen.AddLabel(text='Switch Element Center')
    screen.AddSwitch(value=False, text='Switch Element', align=fase.Switch.CENTER)
    screen.AddLabel(text='Select Left')
    screen.AddSelect(value='First', items=['First', 'Second', 'Third'], align=fase.Select.LEFT)
    screen.AddLabel(text='Select Right')
    screen.AddSelect(value='First', items=['First', 'Second', 'Third'], align=fase.Select.RIGHT)
    screen.AddLabel(text='Select Center')
    screen.AddSelect(value='First', items=['First', 'Second', 'Third'], align=fase.Select.CENTER)
    screen.AddLabel(text='Image Filename 128x128')
    screen.AddImage(filename='images/nyc_128x128.jpg')
    screen.AddLabel(text='Image Filename 240x137')
    screen.AddImage(filename='images/nyc_240x137.jpg')
    screen.AddLabel(text='Image Filename 800x600')
    screen.AddImage(filename='images/nyc_800x600.jpg')
    screen.AddLabel(text='Image Url Small')
    screen.AddImage(url='http://tryourla.com/wp-content/uploads/2010/08/la_skyline.jpg')
    screen.AddLabel(text='Slider')
    screen.AddSlider(value=50., min_value=0., max_value=200., step=5.)
    screen.AddLabel(text='Button Text')
    screen.AddButton(text='Button')
    screen.AddLabel(text='Button Image')
    screen.AddButton(image=fase.Image(url='http://tryourla.com/wp-content/uploads/2010/08/la_skyline.jpg'))
    screen.AddLabel(text='Contact Picker')
    screen.AddContactPicker(hint='Contact Picker')
    screen.AddLabel(text='DateTime Picker Date')
    screen.AddDateTimePicker(hint='DateTime Picker Date', type_=fase.DateTimePicker.DATE)
    screen.AddLabel(text='DateTime Picker Time')
    screen.AddDateTimePicker(hint='DateTime Picker Time', type_=fase.DateTimePicker.TIME)
    screen.AddLabel(text='Place Picker')
    screen.AddPlacePicker(hint='Place Picker', type_=fase.PlacePicker.CITY)
    screen.AddSeparator()
    screen.AddLabel(text='Web')
    screen.AddWeb(url='www.google.com')
    return screen

  def OnSignIn(self, screen, element):
    return fase_sign_in.StartSignIn(
        self, on_done=FaseTestService.OnSignInDone, on_cancel=FaseTestService.OnSignInOutCancel)

  def OnSignInDone(self, user_id_before=None):
    return self.OnStart()

  def OnSignOut(self, screen, element):
    return fase_sign_in.StartSignOut(self, on_cancel=FaseTestService.OnSignInOutCancel)

  def OnSignInOutCancel(self):
    return self.OnStart()


fase.Service.RegisterService(FaseTestService)
