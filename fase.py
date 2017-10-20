import fase_database
import fase_model
import json_util

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'


# TODO(igushev): Move on_click to Element.


def GenerateUserId(device):
  pass


@json_util.JSONDecorator({})
class Variable(object):
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
    {'_id_to_variable_int':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(IntVariable)),
     '_id_to_variable_float':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(FloatVariable)),
     '_id_to_variable_string':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(StringVariable)),
     '_id_to_variable_bool':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(BoolVariable))})
class VariableSet(object):
  def __init__(self):
    self._id_to_variable_int = {}
    self._id_to_variable_float = {}
    self._id_to_variable_string = {}
    self._id_to_variable_bool = {}

  def AddIntVariable(self, id_, value):
    assert id_ not in self._id_to_variable_int
    self._id_to_variable_int[id_] = IntVariable(value)
  def GetIntVariable(self, id_):
    return self._id_to_variable_int[id_]

  def AddFloatVariable(self, id_, value):
    assert id_ not in self._id_to_variable_float
    self._id_to_variable_float[id_] = FloatVariable(value)
  def GetFloatVariable(self, id_):
    return self._id_to_variable_float[id_]

  def AddStringVariable(self, id_, value):
    assert id_ not in self._id_to_variable_string
    self._id_to_variable_string[id_] = StringVariable(value)
  def GetStringVariable(self, id_):
    return self._id_to_variable_string[id_]

  def AddBoolVariable(self, id_, value):
    assert id_ not in self._id_to_variable_bool
    self._id_to_variable_bool[id_] = BoolVariable(value)
  def GetBoolVariable(self, id_):
    return self._id_to_variable_bool[id_]


@json_util.JSONDecorator({}, inherited=True)
class Element(object):
  pass


@json_util.JSONDecorator(
    {'_id_to_element':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(Element))})
class ContainerElement(Element, VariableSet):
  def __init__(self):
    super(ContainerElement, self).__init__()
    self._id_to_element = {}

  def AddElement(self, type_, id_, *args, **kwargs):
    assert id_ not in self._id_to_element
    element = type_(*args, **kwargs)
    self._id_to_element[id_] = element
    return element
  def GetElement(self, id_):
    return self._id_to_element[id_]

  def AddLayout(self, id_, *args, **kwargs):
    return self.AddElement(Layout, id_, *args, **kwargs)
  def GetLayout(self, id_):
    return self.GetElement(id_)

  def AddLabel(self, id_, *args, **kwargs):
    return self.AddElement(Label, id_, *args, **kwargs)
  def GetLabel(self, id_):
    return self.GetElement(id_)

  def AddText(self, id_, *args, **kwargs):
    return self.AddElement(Text, id_, *args, **kwargs)
  def GetText(self, id_):
    return self.GetElement(id_)

  def AddImage(self, id_, *args, **kwargs):
    return self.AddElement(Image, id_, *args, **kwargs)
  def GetImage(self, id_):
    return self.GetElement(id_)


@json_util.JSONDecorator(
    {'_orientation': json_util.JSONInt(),
     '_scrollable': json_util.JSONBool(),
     '_sizable': json_util.JSONInt(),
     '_on_click': json_util.JSONClassMethod()})
class Layout(ContainerElement):
  VERTICAL = 1
  HORIZONTAL = 2

  WRAP_INNER_ELEMENTS = 1
  FIT_OUTER_ELEMENT = 2

  def __init__(self, orientation=None, scrollable=None, sizable=None,
               on_click=None):
    super(Layout, self).__init__()
    self._orientation = orientation
    self._scrollable = scrollable
    self._sizable = sizable
    self._on_click = on_click


@json_util.JSONDecorator(
    {'_label': json_util.JSONString(),
     '_font': json_util.JSONFloat(),
     '_aligh': json_util.JSONInt(),
     '_sizable': json_util.JSONInt()})
class Label(Element):

  LEFT = 1
  CENTER = 2
  RIGHT = 3

  FIXED = 1  
  FIT_OUTER_ELEMENT = 2

  def __init__(self, label=None, font=None, aligh=None, sizable=None):
    self._label = label
    self._font = font
    self._aligh = aligh
    self._sizable = sizable


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_hint': json_util.JSONString(),
     '_sizable': json_util.JSONInt()})
class Text(Element):

  FIXED = 1  
  FIT_OUTER_ELEMENT = 2
  
  def __init__(self, text=None, hint=None, sizable=None):
    self._text = text
    self._hint = hint
    self._sizable = sizable


@json_util.JSONDecorator(
    {'_image': json_util.JSONString()})
class Image(Element):
  
  def __init__(self, image=None):
    self._image = image


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_on_click': json_util.JSONClassMethod(),
     '_on_click_element': json_util.JSONObject(Element),
     '_icon': json_util.JSONString()})
class MenuItem(Element):

  def __init__(self, text=None,
               on_click=None, on_click_element=None, icon=None):
    super(MenuItem, self).__init__()
    self._text = text
    self._on_click = on_click
    self._on_click_element = on_click_element
    self._icon = icon


@json_util.JSONDecorator(
    {'_id_to_menu_item':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(MenuItem))})
class Menu(Element):
  def __init__(self):
    super(Menu, self).__init__()
    self._id_to_menu_item = {}

  def AddMenuItem(self, id_, text=None,
                  on_click=None, on_click_element=None, icon=None):
    assert id_ not in self._id_to_menu_item
    menu_item = MenuItem(text=text, on_click=on_click,
                         on_click_element=on_click_element, icon=icon)
    self._id_to_menu_item[id_] = menu_item
    return menu_item
  def GetMenuItem(self, id_):
    return self._id_to_menu_item[id_]


@json_util.JSONDecorator(
    {'_text': json_util.JSONString(),
     '_on_click': json_util.JSONClassMethod(),
     '_icon': json_util.JSONString()})
class Button(Element):

  def __init__(self, text=None, on_click=None, icon=None):
    super(Button, self).__init__()
    self._text = text
    self._on_click = on_click
    self._icon = icon


@json_util.JSONDecorator(
    {'_id_to_button':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONObject(Button))})
class ButtonBar(Element):
  def __init__(self):
    super(ButtonBar, self).__init__()
    self._id_to_button = {}

  def AddButton(self, id_, text=None, on_click=None, icon=None):
    assert id_ not in self._id_to_button
    button = Button(text=text, on_click=on_click, icon=icon)
    self._id_to_button[id_] = button
    return button
  def GetButton(self, id_):
    return self._id_to_button[id_]
    

@json_util.JSONDecorator(
    {'_text': json_util.JSONString()})
class Popup(Element, VariableSet):

  def __init__(self, text=None):
    self._text = text


@json_util.JSONDecorator(
    {'_menu_displayed': json_util.JSONBool(),
     '_main_button_displayed': json_util.JSONBool(),
     '_button_bar_displayed': json_util.JSONBool(),
     '_next_step_button': json_util.JSONObject(Button),
     '_prev_step_button': json_util.JSONObject(Button),
     '_context_menu': json_util.JSONObject(Menu)})
class Screen(ContainerElement):

  def __init__(self):
    super(Screen, self).__init__()
    self._menu_displayed = True
    self._main_button_displayed = True
    self._button_bar_displayed = True
    self._next_step_button = None
    self._prev_step_button = None
    self._context_menu = None

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
    self._next_step_button = Button(text=text, on_click=on_click, icon=icon)
    return self._next_step_button
  def GetNextStepButton(self):
    assert self._next_step_button is not None
    return self._next_step_button

  def AddPrevStepButton(self, text=None, on_click=None, icon=None):
    self._prev_step_button = Button(text=text, on_click=on_click, icon=icon)
    return self._prev_step_button
  def GetPrevStepButton(self):
    assert self._prev_step_button is not None
    return self._prev_step_button

  def AddContextMenu(self):
    self._context_menu = Menu()
    return self._context_menu
  def GetContextMenu(self):
    assert self._context_menu is not None
    return self._context_menu


@json_util.JSONDecorator(
    {'_menu': json_util.JSONObject(Menu),
     '_main_menu': json_util.JSONObject(Menu),
     '_button_bar': json_util.JSONObject(ButtonBar),
     '_device': json_util.JSONObject(fase_model.Device),
     '_user_id': json_util.JSONString()})
class Service(VariableSet):
  
  service_dict = {}

  @staticmethod
  def RegisterService(service_name, service_obj):
    assert isinstance(service_obj, Service)
    Service.service_dict[service_name] = service_obj

  def __init__(self, device):
    super(Service, self).__init__()
    
    self._menu = None
    self._main_menu = None
    self._button_bar = None
    self._device = device
    self._user_id = GenerateUserId(self._device)

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

  def SetUserId(self, user_id):
    self._user_id = user_id
  def GetUserId(self):
    return self._user_id
  def ResetUserId(self):
    self._user_id = GenerateUserId(self._device)
