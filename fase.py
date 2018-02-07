import datetime
import hashlib
import re

import data_util
import json_util
import util

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'
# Name and Phone Number from Contact List.
CONTACT_FORMAT = '{display_name}|{phone_number}'
CONTACT_REGEXP = '(?P<display_name>.*)\|(?P<phone_number>.*)'

NEXT_STEP_BUTTON_ID = 'next_step_button'
PREV_STEP_BUTTON_ID = 'prev_step_button'
CONTEXT_MENU_ID = 'context_menu'
POPUP_ID = 'popup'
MAIN_MENU_ID = 'main_menu'
MAIN_BUTTON_ID = 'main_button'
BUTTON_BAR_ID = 'button_bar'


def MockFunction():
  pass


def GenerateSessionId():
  datetime_now = datetime.datetime.now()
  session_id_hash = hashlib.md5()
  session_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH).encode('utf-8'))
  session_id = session_id_hash.hexdigest()
  return session_id


def GenerateScreenId(session_id):
  datetime_now = datetime.datetime.now()
  screen_id_hash = hashlib.md5()
  screen_id_hash.update(session_id.encode('utf-8'))
  screen_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH).encode('utf-8'))
  screen_id = screen_id_hash.hexdigest()
  return screen_id


def GenerateUserId(session_id):
  datetime_now = datetime.datetime.now()
  screen_id_hash = hashlib.md5()
  screen_id_hash.update(session_id.encode('utf-8'))
  screen_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH).encode('utf-8'))
  screen_id = screen_id_hash.hexdigest()
  return screen_id


@json_util.JSONDecorator({
    'country_code': json_util.JSONString()})
class Locale(data_util.AbstractObject):

  def __init__(self, country_code):
    self.country_code = country_code


@json_util.JSONDecorator({}, inherited=True)
class Element(data_util.AbstractObject):
  def __init__(self):
    super(Element, self).__init__()

  def FaseOnClick(self, service, screen):
    screen = self._on_click(service, screen, self)
    return service, screen


@json_util.JSONDecorator(
    {'_id_element_list':
     json_util.JSONList(json_util.JSONTuple([json_util.JSONString(),
                                             json_util.JSONObject(Element)]))})
class ElementContainer(Element):
  def __init__(self):
    super(ElementContainer, self).__init__()
    self._id_element_list = []

  def AddElement(self, id_, element):
    assert not self.HasElement(id_)
    self._id_element_list.append((id_, element))
    return element

  def HasElement(self, id_):
    for id_in_list, _ in self._id_element_list:
      if id_in_list == id_:
        return True
    return False

  def GetElement(self, id_):
    for id_in_list, value in self._id_element_list:
      if id_in_list == id_:
        return value
    raise KeyError(id_)

  def PopElement(self, id_):
    for i, (id_in_list, value) in enumerate(self._id_element_list):
      if id_in_list == id_:
        del self._id_element_list[i]
        return value
    raise KeyError(id_)

  def GetIdElementList(self):
    return self._id_element_list


@json_util.JSONDecorator({})
class Variable(Element):
  def __init__(self):
    super(Variable, self).__init__()


@json_util.JSONDecorator(
    {'_value': json_util.JSONInt()})
class IntVariable(Variable):
  def __init__(self, value):
    super(IntVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    util.AssertIsInstanceOrNone(value, int)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator(
    {'_value': json_util.JSONFloat()})
class FloatVariable(Variable):
  def __init__(self, value):
    super(FloatVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    util.AssertIsInstanceOrNone(value, float)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator(
    {'_value': json_util.JSONString()})
class StringVariable(Variable):
  def __init__(self, value):
    super(StringVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    util.AssertIsInstanceOrNone(value, str)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator(
    {'_value': json_util.JSONBool()})
class BoolVariable(Variable):
  def __init__(self, value):
    super(BoolVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    util.AssertIsInstanceOrNone(value, bool)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator(
    {'_value': json_util.JSONFunction()})
class FunctionVariable(Variable):
  def __init__(self, value):
    super(FunctionVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    assert callable(value)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator({})
class VariableContainer(ElementContainer):
  def __init__(self):
    super(VariableContainer, self).__init__()

  def AddIntVariable(self, id_, value):
    return self.AddElement(id_, IntVariable(value))
  def HasIntVariable(self, id_):
    return self.HasElement(id_)
  def GetIntVariable(self, id_):
    return self.GetElement(id_)
  def PopIntVariable(self, id_):
    return self.PopElement(id_)

  def AddFloatVariable(self, id_, value):
    return self.AddElement(id_, FloatVariable(value))
  def HasFloatVariable(self, id_):
    return self.HasElement(id_)
  def GetFloatVariable(self, id_):
    return self.GetElement(id_)
  def PopFloatVariable(self, id_):
    return self.PopElement(id_)

  def AddStringVariable(self, id_, value):
    return self.AddElement(id_, StringVariable(value))
  def HasStringVariable(self, id_):
    return self.HasElement(id_)
  def GetStringVariable(self, id_):
    return self.GetElement(id_)
  def PopStringVariable(self, id_):
    return self.PopElement(id_)

  def AddBoolVariable(self, id_, value):
    return self.AddElement(id_, BoolVariable(value))
  def HasBoolVariable(self, id_):
    return self.HasElement(id_)
  def GetBoolVariable(self, id_):
    return self.GetElement(id_)
  def PopBoolVariable(self, id_):
    return self.PopElement(id_)

  def AddFunctionVariable(self, id_, value):
    return self.AddElement(id_, FunctionVariable(value))
  def HasFunctionVariable(self, id_):
    return self.HasElement(id_)
  def GetFunctionVariable(self, id_):
    return self.GetElement(id_)
  def PopFunctionVariable(self, id_):
    return self.PopElement(id_)


@json_util.JSONDecorator(
    {'_displayed': json_util.JSONBool(),
     '_request_locale': json_util.JSONBool(),
     '_locale': json_util.JSONObject(Locale)})
class VisualElement(VariableContainer):
  def __init__(self):
    super(VisualElement, self).__init__()
    self._displayed = True
    self._request_locale = False
    self._locale = None

  def SetDisplayed(self, displayed):
    self._displayed = displayed
  def GetDisplayed(self):
    return self._displayed

  def SetRequestLocale(self, request_locale):
    self._request_locale = request_locale
  def GetRequestLocale(self):
    return self._request_locale
  def SetLocale(self, locale):
    self._locale = locale
  def GetLocale(self):
    return self._locale


@json_util.JSONDecorator(
    {'_label': json_util.JSONString(),
     '_font': json_util.JSONFloat(),
     '_size': json_util.JSONInt(),
     '_alight': json_util.JSONInt(),
     '_on_click': json_util.JSONFunction()})
class Label(VisualElement):

  MIN = 1
  MAX = 2

  LEFT = 1
  RIGHT = 2
  CENTER = 3

  def __init__(self,
               label=None,
               font=None,
               size=None,
               alight=None,
               on_click=None):
    super(Label, self).__init__()
    self._label = label
    self._font = font
    self._size = size
    self._alight = alight
    self._on_click = on_click

  def GetLabel(self):
    return self._label

  def GetFont(self):
    return self._font

  def GetSize(self):
    return self._size

  def GetAlight(self):
    return self._alight

  def GetOnClick(self):
    return self._on_click


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_hint': json_util.JSONString(),
     '_size': json_util.JSONInt()})
class Text(VisualElement):

  MIN = 1
  MAX = 2
  
  def __init__(self,
               text=None,
               hint=None,
               size=None):
    super(Text, self).__init__()
    self._text = text
    self._hint = hint
    self._size = size

  def Update(self, value):
    self._text = value if value else None
  def Get(self):
    return self._text

  def SetText(self, text):
    self._text = text
  def GetText(self):
    return self._text

  def GetSize(self):
    return self._size


@json_util.JSONDecorator(
    {'_value': json_util.JSONBool(),
     '_text': json_util.JSONString(),
     '_alight': json_util.JSONInt()})
class Switch(VisualElement):

  LEFT = 1
  RIGHT = 2
  CENTER = 3
  
  def __init__(self,
               value=None,
               text=None,
               alight=None):
    super(Switch, self).__init__()
    self._value = value
    self._text = text
    self._alight = alight

  def Update(self, value):
    self._value = bool(value)
  def Get(self):
    return str(self._value)

  def SetValue(self, value):
    self._value = value
  def GetValue(self):
    return self._value

  def GetText(self):
    return self._text

  def GetAlight(self):
    return self._alight


@json_util.JSONDecorator(
    {'_image': json_util.JSONString()})
class Image(VisualElement):

  def __init__(self,
               image=None):
    super(Image, self).__init__()
    self._image = image

  def GetImage(self):
    return self._image


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_on_click': json_util.JSONFunction(),
     '_icon': json_util.JSONString()})
class MenuItem(VisualElement):

  def __init__(self,
               text=None,
               on_click=None,
               icon=None):
    super(MenuItem, self).__init__()
    self._text = text
    self._on_click = on_click
    self._icon = icon

  def GetText(self):
    return self._text

  def GetOnClick(self):
    return self._on_click

  def GetIcon(self):
    return self._icon


@json_util.JSONDecorator({
    '_text': json_util.JSONString()})
class Menu(ElementContainer):
  def __init__(self, text=None):
    super(Menu, self).__init__()
    self._text = text

  def GetText(self):
    return self._text

  def AddMenuItem(self, id_,
                  text=None,
                  on_click=None,
                  icon=None):
    menu_item = MenuItem(text=text,
                         on_click=on_click,
                         icon=icon)
    return self.AddElement(id_, menu_item)
  def GetMenuItem(self, id_):
    return self.GetElement(id_)


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_on_click': json_util.JSONFunction(),
     '_context_menu': json_util.JSONObject(Menu),
     '_icon': json_util.JSONString()})
class Button(VisualElement):

  def __init__(self,
               text=None,
               on_click=None,
               context_menu=None,
               icon=None):
    assert int(on_click is None) + int(context_menu is None) == 1
    super(Button, self).__init__()
    self._text = text
    self._on_click = on_click
    self._context_menu = context_menu
    self._icon = icon

  def SetText(self, text):
    self._text = text
  def GetText(self):
    return self._text

  def GetOnClick(self):
    return self._on_click

  def GetContextMenu(self):
    return self._context_menu

  def GetIcon(self):
    return self._icon

  def GetElement(self, id_):
    if id_ == CONTEXT_MENU_ID:
      return self._context_menu
    return super(Button, self).GetElement(id_)


@json_util.JSONDecorator({})
class ButtonBar(ElementContainer):
  def __init__(self):
    super(ButtonBar, self).__init__()

  def AddButton(self, id_,
                text=None,
                on_click=None,
                icon=None):
    button = Button(text=text,
                    on_click=on_click,
                    icon=icon)
    return self.AddElement(id_, button)
  def GetButton(self, id_):
    return self.GetElement(id_)
    

@json_util.JSONDecorator(
    {'_display_name': json_util.JSONString(),
     '_phone_number': json_util.JSONString(),
     '_hint': json_util.JSONString(),
     '_size': json_util.JSONInt(),
     '_on_pick': json_util.JSONFunction()})
class ContactPicker(VisualElement):

  MIN = 1
  MAX = 2
  
  def __init__(self,
               display_name=None,
               phone_number=None,
               hint=None,
               size=None,
               on_pick=None):
    super(ContactPicker, self).__init__()
    self._display_name = display_name
    self._phone_number = phone_number
    self._hint = hint
    self._size = size
    self._on_pick = on_pick

  def Update(self, value):
    contact_match = re.match(CONTACT_REGEXP, value)
    self._display_name = contact_match.group('display_name') or None
    self._phone_number = contact_match.group('phone_number') or None
  def Get(self):
    return CONTACT_FORMAT.format(display_name=self._display_name or '',
                                 phone_number=self._phone_number or '')    

  def SetDisplayName(self, display_name):
    self._display_name = display_name
  def GetDisplayName(self):
    return self._display_name

  def SetPhoneNumber(self, phone_number):
    self._phone_number = phone_number
  def GetPhoneNumber(self):
    return self._phone_number

  def GetSize(self):
    return self._size

  def GetOnPick(self):
    return self._on_pick

  def FaseOnClick(self, service, screen):
    screen = self._on_pick(service, screen, self)
    return service, screen


@json_util.JSONDecorator({})
class BaseElementsContainer(VisualElement):
  def __init__(self):
    super(BaseElementsContainer, self).__init__()

  def AddLayout(self, id_,
               orientation=None,
               size=None,
               on_click=None,
               border=None):
    return self.AddElement(id_, Layout(orientation=orientation,
                                       size=size,
                                       on_click=on_click,
                                       border=border))
  def GetLayout(self, id_):
    return self.GetElement(id_)

  def AddLabel(self, id_,
               label=None,
               font=None,
               size=None,
               alight=None):
    return self.AddElement(id_, Label(label=label, font=font, size=size, alight=alight))
  def GetLabel(self, id_):
    return self.GetElement(id_)

  def AddText(self, id_,
               text=None,
               hint=None,
               size=None):
    return self.AddElement(id_, Text(text=text, hint=hint, size=size))
  def GetText(self, id_):
    return self.GetElement(id_)

  def AddSwitch(self, id_,
                value=None,
                text=None,
                alight=None):
    return self.AddElement(id_, Switch(value=value, text=text, alight=alight))
  def GetSwitch(self, id_):
    return self.GetElement(id_)

  def AddImage(self, id_,
               image=None):
    return self.AddElement(id_, Image(image=image))
  def GetImage(self, id_):
    return self.GetElement(id_)

  def AddButton(self, id_,
               text=None,
               on_click=None,
               context_menu=None,
               icon=None):
    return self.AddElement(id_, Button(text=text, on_click=on_click, context_menu=context_menu, icon=icon))
  def GetButton(self, id_):
    return self.GetElement(id_)

  def AddContactPicker(self, id_,
                       display_name=None,
                       phone_number=None,
                       hint=None,
                       size=None,
                       on_pick=None):
    return self.AddElement(id_, ContactPicker(display_name=display_name, phone_number=phone_number,
                                              hint=hint, size=size, on_pick=on_pick))
  def GetContactPicker(self, id_):
    return self.GetElement(id_)


@json_util.JSONDecorator(
    {'_orientation': json_util.JSONInt(),
     '_size': json_util.JSONInt(),
     '_on_click': json_util.JSONFunction(),
     '_border': json_util.JSONBool()})
class Layout(BaseElementsContainer):

  VERTICAL = 1
  HORIZONTAL = 2

  MIN = 1
  MAX = 2

  def __init__(self,
               orientation=None,
               size=None,
               on_click=None,
               border=None):
    super(Layout, self).__init__()
    self._orientation = orientation
    self._size = size
    self._on_click = on_click
    self._border = border

  def GetOrientation(self):
    return self._orientation

  def GetSize(self):
    return self._size

  def GetOnClick(self):
    return self._on_click

  def GetBorder(self):
    return self._border


@json_util.JSONDecorator(
    {'_text': json_util.JSONString()})
class Popup(ElementContainer):

  def __init__(self, text=None):
    super(Popup, self).__init__()
    self._text = text

  def GetText(self):
    return self._text

  def AddButton(self, id_,
                text=None,
                on_click=None,
                icon=None):
    button = Button(text=text,
                    on_click=on_click,
                    icon=icon)
    return self.AddElement(id_, button)
  def GetButton(self, id_):
    return self.GetElement(id_)


@json_util.JSONDecorator(
    {'_screen_id': json_util.JSONString(),
     '_scrollable': json_util.JSONBool(),
     '_title': json_util.JSONString()})
class Screen(BaseElementsContainer):

  def __init__(self, service):
    super(Screen, self).__init__()
    self._screen_id = GenerateScreenId(service.GetSessionId())
    self._scrollable = None
    self._title = None

  def UpdateScreenId(self, service):
    self._screen_id = GenerateScreenId(service.GetSessionId())
  def GetScreenId(self):
    return self._screen_id

  def SetScrollable(self, scrollable):
    self._scrollable = scrollable
  def GetScrollable(self):
    return self._scrollable

  def SetTitle(self, title):
    self._title = title
  def GetTitle(self):
    return self._title

  def AddMainMenu(self):
    return self.AddElement(MAIN_MENU_ID, Menu())
  def GetMainMenu(self):
    return self.GetElement(MAIN_MENU_ID)

  def AddMainButton(self, text=None, on_click=None, context_menu=None, icon=None):
    return self.AddElement(MAIN_BUTTON_ID, Button(text=text, on_click=on_click, context_menu=context_menu, icon=icon))
  def GetMainButton(self):
    return self.GetElement(MAIN_BUTTON_ID)

  def AddButtonBar(self):
    return self.AddElement(BUTTON_BAR_ID, ButtonBar())
  def GetButtonBar(self):
    return self.GetElement(BUTTON_BAR_ID)

  def AddNextStepButton(self, text=None, on_click=None, icon=None):
    return self.AddElement(NEXT_STEP_BUTTON_ID, Button(text=text, on_click=on_click, icon=icon))
  def GetNextStepButton(self):
    return self.GetElement(NEXT_STEP_BUTTON_ID)

  def AddPrevStepButton(self, text=None, on_click=None, icon=None):
    return self.AddElement(PREV_STEP_BUTTON_ID, Button(text=text, on_click=on_click, icon=icon))
  def GetPrevStepButton(self):
    return self.GetElement(PREV_STEP_BUTTON_ID)

  def AddContextMenu(self, text=None):
    return self.AddElement(CONTEXT_MENU_ID, Menu(text=text))
  def GetContextMenu(self):
    return self.GetElement(CONTEXT_MENU_ID)

  def AddPopup(self, text=None):
    return self.AddElement(POPUP_ID, Popup(text=text))
  def GetPopup(self):
    return self.GetElement(POPUP_ID) 


@json_util.JSONDecorator(
    {'_session_id': json_util.JSONString(),
     '_if_signed_in': json_util.JSONBool(),
     '_user_phone_number': json_util.JSONString(),
     '_user_name': json_util.JSONString(),
     '_user_id': json_util.JSONString(),
     '_datetime_added': json_util.JSONDateTime()})
class Service(VariableContainer):
  
  service_cls = None

  @staticmethod
  def RegisterService(service_cls):
    assert Service.service_cls is None
    assert issubclass(service_cls, Service)
    Service.service_cls = service_cls

  def __init__(self):
    super(Service, self).__init__()
    self._session_id = GenerateSessionId()
    self._if_signed_in = False
    self._user_id = GenerateUserId(self._session_id)
    self._user_phone_number = None
    self._user_name = None
    self._datetime_added = datetime.datetime.now()

  def GetSessionId(self):
    return self._session_id
  def GetUserId(self):
    return self._user_id
  def IfSignedIn(self):
    return self._if_signed_in
  def GetUserPhoneNumber(self):
    return self._user_phone_number
  def GetUserName(self):
    return self._user_name

