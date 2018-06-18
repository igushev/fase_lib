import shutil
import random

from server_util import version_util

from fase import fase
from fase import fase_sign_in


FASE_TEST_VERSION_FILENAME = 'fase_test_fase/version.txt'
REFRESH_INCREMENT = 10
MORE_INCREMENT = 50



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
  url_version = 1

  @staticmethod
  def Version():
    return FaseTestService.version

  def OnStart(self):
    FaseTestService.UpdateVersionImage()
    FaseTestService.UpdateURLImage()
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
    navigation.AddButton(id_='label_test_button', text='Label Test', on_click=FaseTestService.OnLabelTest)
    navigation.AddButton(id_='image_test_button', text='Image Test', on_click=FaseTestService.OnImageTest)
    navigation.AddButton(id_='vertical_max_size_test_button', text='Vertical Max Size Test',
                         on_click=FaseTestService.OnVerticalMaxSizeTest)
    navigation.AddButton(id_='aligning_buttons_test_button', text='Aligning Buttons Test',
                         on_click=FaseTestService.OnAligningButtonsTest)
    navigation.AddButton(id_='refresh_test_button', text='Refresh Test',
                         on_click=FaseTestService.OnRefreshTest)
    navigation.AddButton(id_='more_test_button', text='More Test',
                         on_click=FaseTestService.OnMoreTest)
    navigation.AddButton(id_='vertical_split_with_separator_test_button', text='Vertical Split With Separator Test',
                         on_click=FaseTestService.OnVerticalSplitWithSeparatorTest)
    navigation.AddButton(id_='vertical_split_no_separator_test_button', text='Vertical Split No Separator Test',
                         on_click=FaseTestService.OnVerticalSplitNoSeparatorTest)
    navigation.AddButton(id_='web_test_test_button', text='Web Test', on_click=FaseTestService.OnWebTest)
    navigation.AddButton(id_='web_and_buttons_max_test_button', text='Web And Buttons Max Test',
                         on_click=FaseTestService.OnWebAndButtonsMaxTest)
    navigation.AddButton(id_='web_and_buttons_scrollable_test_button', text='Web And Buttons Scrollable Test',
                         on_click=FaseTestService.OnWebAndButtonsScrollableTest)
    navigation.AddButton(id_='version_update_test_button', text='Version Update Test',
                         on_click=FaseTestService.OnVersionUpdateTest)
    navigation.AddButton(id_='url_update_test_button', text='URL Update Test',
                         on_click=FaseTestService.OnURLUpdateTest)
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
    screen.AddLabel(text='Label Size 0.5', align=fase.Label.CENTER, font=fase.Font(size=0.5))
    screen.AddLabel(text='Label Size 0.75', align=fase.Label.CENTER, font=fase.Font(size=0.75))
    screen.AddLabel(text='Label Size 1.', align=fase.Label.CENTER, font=fase.Font(size=1.))
    screen.AddLabel(text='Label Size 1.25', align=fase.Label.CENTER, font=fase.Font(size=1.25))
    screen.AddLabel(text='Label Size 1.5', align=fase.Label.CENTER, font=fase.Font(size=1.5))
    screen.AddLabel(text='Label Bold', align=fase.Label.CENTER, font=fase.Font(bold=True))
    screen.AddLabel(text='Label Italic', align=fase.Label.CENTER, font=fase.Font(italic=True))
    screen.AddLabel(text='Label Bold Italic', align=fase.Label.CENTER, font=fase.Font(bold=True, italic=True))
    screen.AddLabel(text='Label Size 1.5 Bold', align=fase.Label.CENTER, font=fase.Font(size=1.5, bold=True))
    screen.AddSeparator()
    screen.AddLabel(text='Text Element Default: Text and Singleline')
    screen.AddText(hint='Text Element')
    screen.AddLabel(text='Text Element Multiline')
    screen.AddText(hint='Text Element Multiline', multiline=True)
    screen.AddLabel(text='Text Element Digits')
    screen.AddText(hint='Text Element', type_=fase.Text.DIGITS)
    screen.AddLabel(text='Text Element Phone')
    screen.AddText(hint='Text Element', type_=fase.Text.PHONE)
    screen.AddLabel(text='Text Element Email')
    screen.AddText(hint='Text Element', type_=fase.Text.EMAIL)
    screen.AddSeparator()
    screen.AddLabel(text='Switch Element Left')
    screen.AddSwitch(value=True, text='Switch Element', align=fase.Switch.LEFT)
    screen.AddLabel(text='Switch Element Center')
    screen.AddSwitch(value=False, text='Switch Element', align=fase.Switch.CENTER)
    screen.AddLabel(text='Switch Element Right')
    screen.AddSwitch(value=True, text='Switch Element', align=fase.Switch.RIGHT)
    screen.AddLabel(text='Select Left')
    screen.AddSelect(items=['First', 'Second', 'Third', 'Four'], align=fase.Select.LEFT)
    screen.AddLabel(text='Select Center')
    screen.AddSelect(items=['First', 'Second', 'Third', 'Four'], align=fase.Select.CENTER)
    screen.AddLabel(text='Select Right')
    screen.AddSelect(items=['First', 'Second', 'Third', 'Four'], align=fase.Select.RIGHT)
    screen.AddLabel(text='Select With Selected Second Value')
    screen.AddSelect(value='Second', items=['First', 'Second', 'Third', 'Four'])
    screen.AddLabel(text='Select With Hint')
    screen.AddSelect(hint='Select a Number', items=['First', 'Second', 'Third', 'Four'])
    screen.AddLabel(text='Select With Hint And Selected Third Value')
    screen.AddSelect(value='Third', hint='Select a Number', items=['First', 'Second', 'Third', 'Four'])
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
    return screen

  def OnLabelTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Label Test')
    screen.SetScrollable(True)
    self._AddButtons(screen)

    note_frame = screen.AddFrame(id_='note_frame', orientation=fase.Frame.VERTICAL, border=True)
    note_header_frame1 = note_frame.AddFrame(
        id_='note_header_frame1', orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    note_header_frame1.AddLabel(
        id_='note_header_label1', text='Header', font=fase.Font(size=1.5), size=fase.Label.MAX, align=fase.Label.LEFT)
    note_header_frame1.AddImage(id_='note_header_image1', filename='images/nyc_128x128.jpg')

    note_header_frame2 = note_frame.AddFrame(
        id_='note_header_frame2', orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    note_header_frame2.AddLabel(id_='note_header_label2', text='Header', font=fase.Font(size=1.5))
    note_header_frame2.AddFrame(id_='note_header_inner_frame2', orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    note_header_frame2.AddImage(id_='note_header_image2', filename='images/nyc_128x128.jpg')

    note_frame.AddLabel(id_='note_frame_label', text='Lot of\nmultiline\ntext', align=fase.Label.LEFT)

    note_frame.AddLabel(text='Below horizontal frame with Label. Label has MAX and RIGHT')
    note_deails_frame1 = note_frame.AddFrame(id_='note_deails_frame1', orientation=fase.Frame.HORIZONTAL)
    note_deails_frame1.AddLabel(
        id_='note_deails_frame_datetime_text1', text='Yesterday', font=fase.Font(size=0.75),
        size=fase.Label.MAX, align=fase.Label.RIGHT)

    note_frame.AddLabel(
        text='Below horizontal frame with Inner Frame and Label. Inner Frame has MAX')
    note_deails_frame2 = note_frame.AddFrame(id_='note_deails_frame2', orientation=fase.Frame.HORIZONTAL)
    note_deails_frame2.AddFrame(id_='note_deails_inner_frame2', orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    note_deails_frame2.AddLabel(id_='note_deails_frame_datetime_text2', text='Yesterday', font=fase.Font(size=0.75))

    note_frame.AddLabel(
        text='Below horizontal frame with Inner Frame and Label. Inner Frame has MAX and Label has MAX and LEFT')
    note_deails_frame3 = note_frame.AddFrame(id_='note_deails_frame3', orientation=fase.Frame.HORIZONTAL)
    note_deails_frame3.AddFrame(id_='note_deails_inner_frame3', orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    note_deails_frame3.AddLabel(
        id_='note_deails_frame_datetime_text3', text='Yesterday', font=fase.Font(size=0.75),
        size=fase.Label.MAX, align=fase.Label.LEFT)

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

  def OnRefreshTest(self, screen, element):
    if not screen.HasIntVariable(id_='refresh_start'):
      screen.AddIntVariable(id_='refresh_start', value=0)
    start = screen.GetIntVariable(id_='refresh_start').GetValue()

    screen = fase.Screen(self)
    screen.SetTitle('Refresh Test')
    self._AddButtons(screen)
    screen.AddLabel(text='Refresh screen to continue numbers')
    for i in range(start, start + REFRESH_INCREMENT):
      screen.AddLabel(id_='label_number_%d' % i, text=str(i))
    screen.SetOnRefresh(FaseTestService.OnRefreshTest)
    screen.AddIntVariable(id_='refresh_start', value=start + REFRESH_INCREMENT)
    return screen

  def OnMoreTest(self, screen, element):
    if not screen.HasIntVariable(id_='more_start'):
      screen.AddIntVariable(id_='more_start', value=0)
    start = screen.GetIntVariable(id_='more_start').GetValue()

    screen = fase.Screen(self)
    screen.SetTitle('More Test')
    screen.SetScrollable(True)
    self._AddButtons(screen)
    screen.AddLabel(text='Scroll screen to continue numbers')
    for i in range(start, start + MORE_INCREMENT):
      screen.AddLabel(id_='label_number_%d' % i, text=str(i))
    screen.SetOnMore(FaseTestService.OnMoreTest)
    screen.AddIntVariable(id_='more_start', value=start + MORE_INCREMENT)
    return screen

  @staticmethod
  def _AddLabelAndImage(screen, separator=False):
    for i in range(2):
      frame_outer = screen.AddFrame(id_='frame_outer_%d' % i, orientation=fase.Frame.HORIZONTAL)
      frame_left = frame_outer.AddFrame(id_='frame_left', orientation=fase.Frame.VERTICAL)
      frame_left.AddLabel(text='New York City', align=fase.Label.LEFT)
      frame_left.AddLabel(text='Population: 8 m', align=fase.Label.LEFT)
      frame_left.AddLabel(text='Rank: %d' % i, align=fase.Label.LEFT)
      if separator:
        frame_outer.AddSeparator()
      frame_right = frame_outer.AddFrame(id_='frame_right', orientation=fase.Frame.VERTICAL)
      frame_right.AddImage(filename='images/nyc_800x600.jpg')
    return screen

  def OnVerticalSplitWithSeparatorTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Vertical Split With Separator Test')
    self._AddButtons(screen)
    return FaseTestService._AddLabelAndImage(screen, separator=True)

  def OnVerticalSplitNoSeparatorTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Vertical Split No Separator Test')
    self._AddButtons(screen)
    return FaseTestService._AddLabelAndImage(screen, separator=False)

  def OnWebTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Web Test')
    self._AddButtons(screen)
    screen.AddWeb(url='http://www.apple.com', size=fase.Web.MAX)
    return screen

  def OnWebAndButtonsMaxTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Web And Buttons Max Test')
    screen.AddWeb(url='http://www.apple.com', size=fase.Web.MAX)
    frame_button = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame_button.AddButton(text='Decline', on_click=FaseTestService.StartScreen)
    frame_button.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    frame_button.AddButton(text='Agree', on_click=FaseTestService.StartScreen)
    return screen

  def OnWebAndButtonsScrollableTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Web And Buttons Scrollable Test')
    screen.SetScrollable(True)
    screen.AddWeb(url='http://www.apple.com')
    frame_button = screen.AddFrame(orientation=fase.Frame.HORIZONTAL)
    frame_button.AddButton(text='Decline', on_click=FaseTestService.StartScreen)
    frame_button.AddFrame(orientation=fase.Frame.HORIZONTAL, size=fase.Frame.MAX)
    frame_button.AddButton(text='Agree', on_click=FaseTestService.StartScreen)
    return screen

  def OnVersionUpdateTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('Version Update')
    self._AddButtons(screen)
    screen.AddLabel(text='Version %s' % version_util.ReadVersion(FASE_TEST_VERSION_FILENAME))
    screen.AddImage(filename='images/delete_16_00.png')
    screen.AddLabel(text='Click button below and version will be updated, picture replaced with different color')
    screen.AddButton(text='Update', align=fase.Button.CENTER, on_click=FaseTestService.UpdateVersion)
    return screen

  def UpdateVersion(self, screen, element):
    FaseTestService.version = version_util.ReadAndUpdateVersion(FASE_TEST_VERSION_FILENAME, -1)
    FaseTestService.UpdateVersionImage()
    return self.StartScreen(None, None)

  @staticmethod
  def UpdateVersionImage():
    if int(FaseTestService.version[-1]) % 2 == 0:
      shutil.copyfile('fase_test_fase/images/delete_color_16_00.png', 'fase_test_fase/images/delete_16_00.png')
    else:
      shutil.copyfile('fase_test_fase/images/delete_solid_blue_16_00.png', 'fase_test_fase/images/delete_16_00.png')

  def OnURLUpdateTest(self, screen, element):
    screen = fase.Screen(self)
    screen.SetTitle('URL Update Test')
    self._AddButtons(screen)
    screen.AddImage(url=('http://fase-test-fase-env-test1.us-west-2.elasticbeanstalk.com/'
                         'getresource/filename/images/settings_16_00.png'))
    screen.AddLabel(text='Click button below and picture by URL will be replaced with different color')
    screen.AddButton(text='Update', align=fase.Button.CENTER, on_click=FaseTestService.UpdateURL)
    return screen

  def UpdateURL(self, screen, element):
    FaseTestService.url_version += 1
    FaseTestService.UpdateURLImage()
    return self.StartScreen(None, None)

  @staticmethod
  def UpdateURLImage():
    if FaseTestService.url_version % 2 == 0:
      shutil.copyfile('fase_test_fase/images/settings_color_16_00.png', 'fase_test_fase/images/settings_16_00.png')
    else:
      shutil.copyfile('fase_test_fase/images/settings_solid_blue_16_00.png', 'fase_test_fase/images/settings_16_00.png')

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
    return self.StartScreen(None, None)

  def OnSignOut(self, screen, element):
    return fase_sign_in.StartSignOut(self, on_cancel=FaseTestService.OnSignInOutCancel)

  def OnSignInOutCancel(self):
    return self.StartScreen(None, None)


fase.Service.RegisterService(FaseTestService)
