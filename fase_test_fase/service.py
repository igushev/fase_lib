from server_util import version_util

from fase import fase
from fase import fase_sign_in


FASE_TEST_VERSION_FILENAME = 'fase_test_fase/version.txt'


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

  version = version_util.ReadVersion(FASE_TEST_VERSION_FILENAME)

  @staticmethod
  def Version():
    return FaseTestService.version

  def OnStart(self):
    return self.StartScreen(None, None)

  def StartScreen(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('FaseTest')
    screen.SetScrollable(True)
    self._AddButtons(screen)
    return screen

  def _AddButtons(self, screen):
    navigation = screen.AddNavigation()
    navigation.AddButton(id_='layout_test_button', text='Layout Test', on_click=FaseTestService.OnLayoutTest)
    navigation.AddButton(id_='image_test_button', text='Image Test', on_click=FaseTestService.OnImageTest)
    navigation.AddButton(id_='vertical_max_size_test_button', text='Vertical Max Size Test',
                         on_click=FaseTestService.OnVerticalMaxSizeTest)
    navigation.AddButton(id_='aligning_buttons_test_button', text='Aligning Buttons Test',
                         on_click=FaseTestService.OnAligningButtonsTest)
    navigation.AddButton(id_='label_and_image_test_button', text='Label And Image Test',
                         on_click=FaseTestService.OnLabelAndImageTest)
    navigation.AddButton(id_='web_test_test_button', text='Web Test', on_click=FaseTestService.OnWebTest)
    navigation.AddButton(id_='web_and_buttons_max_test_button', text='Web And Buttons Max Test',
                         on_click=FaseTestService.OnWebAndButtonsMaxTest)
    navigation.AddButton(id_='web_and_buttons_scrollable_test_button', text='Web And Buttons Scrollable Test',
                         on_click=FaseTestService.OnWebAndButtonsScrollableTest)
    navigation.AddButton(id_='error_test_button', text='Error Test', on_click=FaseTestService.OnErrorTest)
    if self.IfSignedIn():
      navigation.AddButton(id_='sign_out_button', text='Sign Out', on_click=FaseTestService.OnSignOut)
    else:
      navigation.AddButton(id_='sign_in_button', text='Sign In', on_click=FaseTestService.OnSignIn)

  def OnLayoutTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Layout Test')
    screen.SetScrollable(True)
    self._AddButtons(screen)
    screen.AddLabel(text='Label Left', align=fase.Label.LEFT)
    screen.AddLabel(text='Label Center', align=fase.Label.CENTER)
    screen.AddLabel(text='Label Right', align=fase.Label.RIGHT)
    screen.AddLabel(text='Label Clickable', on_click=FaseTestService.StartScreen)
    screen.AddLabel(text='Text Element Singline')
    screen.AddText(hint='Text Element')
    screen.AddLabel(text='Text Element Multiline')
    screen.AddText(hint='Text Element Multiline', multiline=True)
    screen.AddLabel(text='Switch Element Left')
    screen.AddSwitch(value=True, text='Switch Element', align=fase.Switch.LEFT)
    screen.AddLabel(text='Switch Element Center')
    screen.AddSwitch(value=False, text='Switch Element', align=fase.Switch.CENTER)
    screen.AddLabel(text='Switch Element Right')
    screen.AddSwitch(value=True, text='Switch Element', align=fase.Switch.RIGHT)
    screen.AddLabel(text='Select Left')
    screen.AddSelect(value='First', items=['First', 'Second', 'Third'], align=fase.Select.LEFT)
    screen.AddLabel(text='Select Center')
    screen.AddSelect(value='First', items=['First', 'Second', 'Third'], align=fase.Select.CENTER)
    screen.AddLabel(text='Select Right')
    screen.AddSelect(value='First', items=['First', 'Second', 'Third'], align=fase.Select.RIGHT)
    screen.AddLabel(text='Slider')
    screen.AddSlider(value=50., min_value=0., max_value=200., step=5.)
    screen.AddLabel(text='Button Text Left')
    screen.AddButton(text='Button', align=fase.Label.LEFT)
    screen.AddLabel(text='Button Text Center')
    screen.AddButton(text='Button', align=fase.Label.CENTER)
    screen.AddLabel(text='Button Text Right')
    screen.AddButton(text='Button', align=fase.Label.RIGHT)
    screen.AddLabel(text='Button Image Filename 128x128')
    screen.AddButton(image=fase.Image(filename='images/nyc_128x128.jpg'))
    screen.AddLabel(text='Button Image Filename 240x137')
    screen.AddButton(image=fase.Image(filename='images/nyc_240x137.jpg'))
    screen.AddLabel(text='Button Image Filename 800x600')
    screen.AddButton(image=fase.Image(filename='images/nyc_800x600.jpg'))
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
    screen.AddWeb(url='http://www.google.com')
    return screen

  def OnImageTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Image Test')
    screen.SetScrollable(True)
    self._AddButtons(screen)
    screen.AddLabel(text='Image Filename 128x128')
    screen.AddImage(filename='images/nyc_128x128.jpg')
    screen.AddLabel(text='Image Filename 240x137')
    screen.AddImage(filename='images/nyc_240x137.jpg')
    screen.AddLabel(text='Image Filename 800x600')
    screen.AddImage(filename='images/nyc_800x600.jpg')
    screen.AddLabel(text='Image Filename 3000x2000')
    screen.AddImage(filename='images/nyc_national_geographic_3000x2000.jpg')
    screen.AddLabel(text='Image Url Small')
    screen.AddImage(url='http://tryourla.com/wp-content/uploads/2010/08/la_skyline.jpg')
    screen.AddLabel(text='Image Filename 128x128 Left')
    screen.AddImage(filename='images/nyc_128x128.jpg', align=fase.Image.LEFT)
    screen.AddLabel(text='Image Filename 128x128 Center')
    screen.AddImage(filename='images/nyc_128x128.jpg', align=fase.Image.CENTER)
    screen.AddLabel(text='Image Filename 128x128 Right')
    screen.AddImage(filename='images/nyc_128x128.jpg', align=fase.Image.RIGHT)
    screen.AddLabel(text='Image Filename 128x128 Clickable')
    screen.AddImage(filename='images/nyc_128x128.jpg', on_click=FaseTestService.StartScreen)
    return screen

  def OnVerticalMaxSizeTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Vertical Max Size Test')
    self._AddButtons(screen)
    screen.AddLabel(text='Two Text Field are Max Size')
    screen.AddText(text='Text 1', multiline=True, size=fase.Text.MAX)
    screen.AddText(text='Text 2', multiline=True, size=fase.Text.MAX)
    return screen

  def OnAligningButtonsTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Aligning Buttons Test')
    self._AddButtons(screen)
    screen.AddLabel(text='Two Buttons on Right Side')
    frame1 = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame1.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    frame1.AddButton(text='Button1')
    frame1.AddButton(text='Button2')
    screen.AddLabel(text='Two Buttons on Sides')
    frame2 = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame2.AddButton(text='Button1')
    frame2.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    frame2.AddButton(text='Button2')
    screen.AddLabel(text='Two Buttons on Left Side')
    frame3 = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame3.AddButton(text='Button1')
    frame3.AddButton(text='Button2')
    frame3.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    return screen

  def OnLabelAndImageTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Label And Image Test')
    self._AddButtons(screen)
    frame_outer = screen.AddFrame(id_='frame_outer', orientation=fase.Frame.HORIZONTAL)
    frame_left = frame_outer.AddFrame(id_='frame_left', orientation=fase.Frame.VERTICAL)
    frame_left.AddLabel(text='New York City', align=fase.Label.LEFT)
    frame_left.AddLabel(text='Population: 8 m', align=fase.Label.LEFT)
    frame_left.AddLabel(text='Rank: 1', align=fase.Label.LEFT)
    frame_right = frame_outer.AddFrame(id_='frame_right', orientation=fase.Frame.VERTICAL)
    frame_right.AddImage(filename='images/nyc_800x600.jpg')
    return screen

  def OnWebTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Web Test')
    self._AddButtons(screen)
    screen.AddWeb(url='http://www.bmwusa.com', size=fase.Web.MAX)
    return screen

  def OnWebAndButtonsMaxTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Web And Buttons Max Test')
    screen.AddWeb(url='http://www.bmwusa.com', size=fase.Web.MAX)
    frame_button = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame_button.AddButton(text='Decline', on_click=FaseTestService.StartScreen)
    frame_button.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    frame_button.AddButton(text='Agree', on_click=FaseTestService.StartScreen)
    return screen

  def OnWebAndButtonsScrollableTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Web And Buttons Scrollable Test')
    screen.SetScrollable(True)
    screen.AddWeb(url='http://www.bmwusa.com')
    frame_button = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame_button.AddButton(text='Decline', on_click=FaseTestService.StartScreen)
    frame_button.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    frame_button.AddButton(text='Agree', on_click=FaseTestService.StartScreen)
    return screen
    
  def OnErrorTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Error Test')
    self._AddButtons(screen)
    screen.AddButton(text='Click to make 500 error', on_click=FaseTestService.MakeError)
    return screen

  def MakeError(self):
    pass

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
