import datetime
import hashlib

import data_util
import fase_database
import json_util

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'


def GenerateSessionId():
  datetime_now = datetime.datetime.now()
  session_id_hash = hashlib.md5()
  session_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH))
  session_id = session_id_hash.hexdigest()
  return session_id


def GenerateScreenId():
  datetime_now = datetime.datetime.now()
  screen_id_hash = hashlib.md5()
  screen_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH))
  screen_id = screen_id_hash.hexdigest()
  return screen_id


@json_util.JSONDecorator({}, inherited=True)
class Element(data_util.AbstractObject):

  def FaseOnClick(self, service, screen):
    screen = self._on_click(service, screen, self)
    return service, screen


@json_util.JSONDecorator(
    {'_id_to_element':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(Element))})
class ElementContainer(Element):
  def __init__(self):
    super(ElementContainer, self).__init__()
    self._id_to_element = {}

  def AddElement(self, id_, element):
    assert id_ not in self._id_to_element
    self._id_to_element[id_] = element
    return element

  def GetElement(self, id_):
    return self._id_to_element[id_]

  def GetIdToElement(self):
    return self._id_to_element


@json_util.JSONDecorator({})
class Variable(Element):
  pass


@json_util.JSONDecorator(
    {'_value': json_util.JSONInt()})
class IntVariable(Variable):
  def __init__(self, value):
    super(IntVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    assert isinstance(value, int)
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
    assert isinstance(value, float)
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
    assert isinstance(value, basestring)
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
    assert isinstance(value, bool)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator(
    {'_value': json_util.JSONClassMethod()})
class ClassMethodVariable(Variable):
  def __init__(self, value):
    super(ClassMethodVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    assert callable(value)
    self._value = value
  def GetValue(self):
    return self._value


@json_util.JSONDecorator({})
class VariableContainer(ElementContainer):

  def AddIntVariable(self, id_, value):
    return self.AddElement(id_, IntVariable(value))
  def GetIntVariable(self, id_):
    return self.GetElement(id_)

  def AddFloatVariable(self, id_, value):
    return self.AddElement(id_, FloatVariable(value))
  def GetFloatVariable(self, id_):
    return self.GetElement(id_)

  def AddStringVariable(self, id_, value):
    return self.AddElement(id_, StringVariable(value))
  def GetStringVariable(self, id_):
    return self.GetElement(id_)

  def AddBoolVariable(self, id_, value):
    return self.AddElement(id_, BoolVariable(value))
  def GetBoolVariable(self, id_):
    return self.GetElement(id_)

  def AddClassMethodVariable(self, id_, value):
    return self.AddElement(id_, ClassMethodVariable(value))
  def GetClassMethodVariable(self, id_):
    return self.GetElement(id_)


class VisualElement(ElementContainer):
  pass

@json_util.JSONDecorator(
    {'_label': json_util.JSONString(),
     '_font': json_util.JSONFloat(),
     '_aligh': json_util.JSONInt(),
     '_sizable': json_util.JSONInt()})
class Label(VisualElement):

  LEFT = 1
  CENTER = 2
  RIGHT = 3

  FIXED = 1  
  FIT_OUTER_ELEMENT = 2

  def __init__(self,
               label=None,
               font=None,
               aligh=None,
               sizable=None):
    self._label = label
    self._font = font
    self._aligh = aligh
    self._sizable = sizable

  def GetLabel(self):
    return self._label


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_hint': json_util.JSONString(),
     '_sizable': json_util.JSONInt()})
class Text(VisualElement):

  FIXED = 1  
  FIT_OUTER_ELEMENT = 2
  
  def __init__(self,
               text=None,
               hint=None,
               sizable=None):
    self._text = text
    self._hint = hint
    self._sizable = sizable

  def Update(self, value):
    self._text = value

  def GetText(self):
    return self._text


@json_util.JSONDecorator(
    {'_image': json_util.JSONString()})
class Image(VisualElement):
  
  def __init__(self,
               image=None):
    self._image = image


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_on_click': json_util.JSONClassMethod(),
     '_on_click_element': json_util.JSONObject(Element),
     '_icon': json_util.JSONString()})
class MenuItem(VisualElement):

  def __init__(self,
               text=None,
               on_click=None,
               on_click_element=None,
               icon=None):
    super(MenuItem, self).__init__()
    self._text = text
    self._on_click = on_click
    self._on_click_element = on_click_element
    self._icon = icon


@json_util.JSONDecorator({})
class Menu(ElementContainer):

  def AddMenuItem(self, id_,
                  text=None,
                  on_click=None,
                  on_click_element=None,
                  icon=None):
    menu_item = MenuItem(text=text,
                         on_click=on_click,
                         on_click_element=on_click_element,
                         icon=icon)
    return self.AddElement(id_, menu_item)
  def GetMenuItem(self, id_):
    return self.GetElement(id_)


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_on_click': json_util.JSONClassMethod(),
     '_icon': json_util.JSONString()})
class Button(VisualElement):

  def __init__(self,
               text=None,
               on_click=None,
               icon=None):
    super(Button, self).__init__()
    self._text = text
    self._on_click = on_click
    self._icon = icon


@json_util.JSONDecorator({})
class ButtonBar(ElementContainer):

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
    

@json_util.JSONDecorator({})
class VisualElementContainer(VariableContainer):

  def AddLayout(self, id_,
               orientation=None,
               scrollable=None,
               sizable=None,
               on_click=None):
    return self.AddElement(id_, Layout(orientation=orientation,
                                       scrollable=scrollable,
                                       sizable=sizable,
                                       on_click=on_click))
  def GetLayout(self, id_):
    return self.GetElement(id_)

  def AddLabel(self, id_,
               label=None,
               font=None,
               aligh=None,
               sizable=None):
    return self.AddElement(id_, Label(label=label, font=font, aligh=aligh, sizable=sizable))
  def GetLabel(self, id_):
    return self.GetElement(id_)

  def AddText(self, id_,
               text=None,
               hint=None,
               sizable=None):
    return self.AddElement(id_, Text(text=text, hint=hint, sizable=sizable))
  def GetText(self, id_):
    return self.GetElement(id_)

  def AddImage(self, id_,
               image=None):
    return self.AddElement(id_, Image(image=image))
  def GetImage(self, id_):
    return self.GetElement(id_)

  def AddButton(self, id_,
               text=None,
               on_click=None,
               icon=None):
    return self.AddElement(id_, Button(text=text, on_click=on_click, icon=icon))
  def GetButton(self, id_):
    return self.GetElement(id_)


@json_util.JSONDecorator(
    {'_orientation': json_util.JSONInt(),
     '_scrollable': json_util.JSONBool(),
     '_sizable': json_util.JSONInt(),
     '_on_click': json_util.JSONClassMethod()})
class Layout(VisualElementContainer):
  VERTICAL = 1
  HORIZONTAL = 2

  WRAP_INNER_ELEMENTS = 1
  FIT_OUTER_ELEMENT = 2

  def __init__(self,
               orientation=None,
               scrollable=None,
               sizable=None,
               on_click=None):
    super(Layout, self).__init__()
    self._orientation = orientation
    self._scrollable = scrollable
    self._sizable = sizable
    self._on_click = on_click


@json_util.JSONDecorator(
    {'_text': json_util.JSONString()})
class Popup(VariableContainer):

  def __init__(self, text=None):
    self._text = text

  def GetText(self):
    return self._text


@json_util.JSONDecorator(
    {'_menu_displayed': json_util.JSONBool(),
     '_main_button_displayed': json_util.JSONBool(),
     '_button_bar_displayed': json_util.JSONBool(),
     '_next_step_button': json_util.JSONObject(Button),
     '_prev_step_button': json_util.JSONObject(Button),
     '_context_menu': json_util.JSONObject(Menu),
     '_popup': json_util.JSONObject(Popup),
     '_session_id': json_util.JSONString(),
     '_screen_id': json_util.JSONString()})
class Screen(VisualElementContainer):

  def __init__(self, service):
    super(Screen, self).__init__()
    self._session_id = service.GetSessionId()
    self._screen_id = GenerateScreenId()
    self._menu_displayed = True
    self._main_button_displayed = True
    self._button_bar_displayed = True
    self._next_step_button = None
    self._prev_step_button = None
    self._context_menu = None
    self._popup = None

  def GetSessionId(self):
    return self._session_id
  def GetScreenId(self):
    return self._screen_id

  def SetMenuDisplayed(self, if_displayed):
    self._menu_displayed = if_displayed
  def GetMenuDisplayed(self):
    return self._menu_displayed
  def SetMainButton(self, if_displayed):
    self._main_button_displayed = if_displayed
  def GetMainButton(self):
    return self._main_button_displayed
  def SetButtonBarDisplayed(self, if_displayed):
    self._button_bar_displayed = if_displayed
  def GetButtonBarDisplayed(self):
    return self._button_bar_displayed

  def AddNextStepButton(self, text=None, on_click=None, icon=None):
    assert self._next_step_button is None
    self._next_step_button = Button(text=text, on_click=on_click, icon=icon)
    return self._next_step_button
  def GetNextStepButton(self):
    assert self._next_step_button is not None
    return self._next_step_button

  def AddPrevStepButton(self, text=None, on_click=None, icon=None):
    assert self._prev_step_button is None
    self._prev_step_button = Button(text=text, on_click=on_click, icon=icon)
    return self._prev_step_button
  def GetPrevStepButton(self):
    assert self._prev_step_button is not None
    return self._prev_step_button

  def AddContextMenu(self):
    assert self._context_menu is None
    self._context_menu = Menu()
    return self._context_menu
  def GetContextMenu(self):
    assert self._context_menu is not None
    return self._context_menu

  def AddPopup(self, text=None):
    assert self._popup is None
    self._popup = Popup(text=text)
    return self._popup
  def GetPopup(self):
    assert self._popup is not None
    return self._popup


@json_util.JSONDecorator(
    {'_menu': json_util.JSONObject(Menu),
     '_main_menu': json_util.JSONObject(Menu),
     '_button_bar': json_util.JSONObject(ButtonBar),
     '_session_id': json_util.JSONString(),
     '_datetime_added': json_util.JSONBool()})
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
    self._menu = None
    self._main_menu = None
    self._button_bar = None
    self._datetime_added = None

  def GetSessionId(self):
    return self._session_id
  def GetUserId(self):
    return self._session_id

  def AddMenu(self):
    self._menu = Menu()
    return self._menu
  def GetMenu(self):
    assert self._menu is not None
    return self._menu

  def AddMainButton(self, text=None, on_click=None, icon=None):
    self._main_menu = Button(text=text, on_click=on_click, icon=icon)
    return self._main_menu
  def GetMainButton(self):
    assert self._main_menu is not None
    return self._main_menu

  def AddButtonBar(self):
    self._button_bar = ButtonBar()
    return self._button_bar
  def GetButtonBar(self):
    assert self._button_bar is not None
    return self._button_bar
