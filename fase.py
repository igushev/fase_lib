import fase_database
import fase_model
import fase_util

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'


class Variable(object):
  pass


class GeneralVariable(Variable):
  def __init__(self, type_, value):
    super(GeneralVariable, self).__init__()
    self._type = type_
    self.SetValue(value)

  def SetValue(self, value):
    assert isinstance(value, self._type)
    self._value = value
  def GetValue(self):
    return self._value


class VariableSet(object):
  def __init__(self):
    self._id_to_variable = {}

  def AddVariable(self, id_, type_, value):
    assert id_ not in self._id_to_variable
    variable = GeneralVariable(type_, value)
    self._id_to_variable[id_] = variable
  def GetVariable(self, id_):
    return self._id_to_variable[id_]

  def AddIntVariable(self, id_, value):
    return self.AddVariable(id_, int, value)
  def GetIntVariable(self, id_):
    return self.GetVariable(id_)

  def AddFloatVariable(self, id_, value):
    return self.AddVariable(id_, float, value)
  def GetFloatVariable(self, id_):
    return self.GetVariable(id_)

  def AddStringVariable(self, id_, value):
    return self.AddVariable(id_, str, value)
  def GetStringVariable(self, id_):
    return self.GetVariable(id_)

  def AddBooleanVariable(self, id_, value):
    return self.AddVariable(id_, bool, value)
  def GetBooleanVariable(self, id_):
    return self.GetVariable(id_)


class Element(object):
  pass


class ContainerElement(Element):
  def __init__(self):
    super(ContainerElement, self).__init__()
    self._id_to_element = {}

  def AddElement(self, id_, type_, *args, **kwargs):
    assert id_ not in self._id_to_element
    element = type_(*args, **kwargs)
    self._id_to_element[id_] = element
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
    return self.AddElement(Text, *args, **kwargs)
  def GetText(self, id_):
    return self.GetElement(id_)


class Layout(ContainerElement):
  VERTICAL = 1
  HORIZONTAL = 2

  WRAP_INNER_ELEMENTS = 1
  FIT_OUTER_ELEMENT = 2

  def __init__(self, orientation=None, scrollable=None, sizable=None):
    super(Layout, self).__init__()
    self._orientation = orientation
    self._scrollable = scrollable
    self._sizable = sizable


class Label(Element):

  FIXED = 1  
  FIT_OUTER_ELEMENT = 2

  def __init__(self, label=None, font=None, aligh=None, sizable=None):
    self._label = label
    self._font = font
    self._aligh = aligh
    self._sizable = sizable


class Text(Element):

  FIXED = 1  
  FIT_OUTER_ELEMENT = 2
  
  def __init__(self, text=None, hint=None, sizable=None):
    self._text = text
    self._hint = hint
    self._sizable = sizable


class Menu(Element):
  def __init__(self):
    super(Menu, self).__init__()
    self._id_to_menu_item = []

  def AddMenuItem(self, id_, text=None, on_click=None, icon=None):
    assert id_ not in self._id_to_menu_item
    menu_item = MenuItem(text=text, on_click=on_click, icon=icon)
    self._id_to_menu_item[id_] = menu_item
    return menu_item
  def GetMenuItem(self, id_):
    return self._id_to_menu_item[id_]


def MenuItem(Element):

  def __init__(self, text=None, on_click=None, icon=None):
    super(MenuItem, self).__init__()
    self._text = text
    self._on_click = on_click
    self._icon = icon


class ButtonBar(Element):
  def __init__(self):
    super(ButtonBar, self).__init__()
    self._id_to_button = []

  def AddButton(self, id_, text=None, on_click=None, icon=None):
    assert id_ not in self._id_to_button
    button = Button(text=text, on_click=on_click, icon=icon)
    self._id_to_button[id_] = button
    return button
  def GetButton(self, id_):
    return self._id_to_button[id_]


def Button(Element):

  def __init__(self, text=None, on_click=None, icon=None):
    super(Button, self).__init__()
    self._text = text
    self._on_click = on_click
    self._icon = icon
    

def Popup(VariableSet):

  def __init__(self, text=None):
    self._text = text


class Screen(ContainerElement, VariableSet):

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
    self._user_id = fase_util.GenerateUserId(self._device)

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
    self._user_id = fase_util.GenerateUserId(self._device)
