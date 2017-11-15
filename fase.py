import datetime
import hashlib

import data_util
import json_util

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'

NEXT_STEP_BUTTON_ID = 'next_step_button'
PREV_STEP_BUTTON_ID = 'prev_step_button'
CONTEXT_MENU_ID = 'context_menu'
POPUP_ID = 'popup'
MENU_ID = 'menu'
MAIN_MENU_ID = 'main_menu'
BUTTON_BAR_ID = 'button_bar'


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
  def __init__(self):
    super(Element, self).__init__()

  def FaseOnClick(self, service, screen):
    screen = self._on_click(service, screen, self)
    return service, screen


# TODO(igushev): Reuse object when deserialized.
@json_util.JSONDecorator(
    {'_id_to_element':
     json_util.JSONDict(json_util.JSONString(), json_util.JSONObject(Element)),
     '_id_element_list':
     json_util.JSONList(json_util.JSONTuple([json_util.JSONString(),
                                             json_util.JSONObject(Element)]))})
class ElementContainer(Element):
  def __init__(self):
    super(ElementContainer, self).__init__()
    self._id_to_element = {}
    self._id_element_list = []

  def AddElement(self, id_, element):
    assert id_ not in self._id_to_element
    self._id_to_element[id_] = element
    self._id_element_list.append((id_, element))
    return element

  def HasElement(self, id_):
    return id_ in self._id_to_element

  def GetElement(self, id_):
    return self._id_to_element[id_]

  def PopElement(self, id_):
    for i, (id_in_list, _) in enumerate(self._id_element_list):
      if id_in_list == id_:
        del self._id_element_list[i]
        break
    return self._id_to_element.pop(id_)

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
    assert isinstance(value, int) or value is None
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
    assert isinstance(value, float) or value is None
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
    assert isinstance(value, basestring) or value is None
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
    assert isinstance(value, bool) or value is None
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
  def __init__(self):
    super(VariableContainer, self).__init__()

  def AddIntVariable(self, id_, value):
    return self.AddElement(id_, IntVariable(value))
  def GetIntVariable(self, id_):
    return self.GetElement(id_)
  def PopIntVariable(self, id_):
    return self.PopElement(id_)

  def AddFloatVariable(self, id_, value):
    return self.AddElement(id_, FloatVariable(value))
  def GetFloatVariable(self, id_):
    return self.GetElement(id_)
  def PopFloatVariable(self, id_):
    return self.PopElement(id_)

  def AddStringVariable(self, id_, value):
    return self.AddElement(id_, StringVariable(value))
  def GetStringVariable(self, id_):
    return self.GetElement(id_)
  def PopStringVariable(self, id_):
    return self.PopElement(id_)

  def AddBoolVariable(self, id_, value):
    return self.AddElement(id_, BoolVariable(value))
  def GetBoolVariable(self, id_):
    return self.GetElement(id_)
  def PopBoolVariable(self, id_):
    return self.PopElement(id_)

  def AddClassMethodVariable(self, id_, value):
    return self.AddElement(id_, ClassMethodVariable(value))
  def GetClassMethodVariable(self, id_):
    return self.GetElement(id_)
  def PopClassMethodVariable(self, id_):
    return self.PopElement(id_)


@json_util.JSONDecorator(
    {'_displayed': json_util.JSONBool()})
class VisualElement(ElementContainer):
  def __init__(self):
    super(VisualElement, self).__init__()
    self._displayed = True

  def SetDisplayed(self, displayed):
    assert isinstance(displayed, bool)
    self._displayed = displayed


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
    super(Label, self).__init__()
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
    super(Text, self).__init__()
    self._text = text
    self._hint = hint
    self._sizable = sizable

  def Update(self, value):
    self._text = value

  def SetText(self, value):
    self._text = value

  def GetText(self):
    return self._text


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
     '_on_click': json_util.JSONClassMethod(),
     '_on_click_element': json_util.JSONObject(Element),
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


@json_util.JSONDecorator({})
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
    

@json_util.JSONDecorator({})
class VisualElementContainer(VariableContainer):
  def __init__(self):
    super(VisualElementContainer, self).__init__()

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
    super(Popup, self).__init__()
    self._text = text

  def GetText(self):
    return self._text


@json_util.JSONDecorator(
    {'_session_id': json_util.JSONString(),
     '_screen_id': json_util.JSONString()})
class Screen(VisualElementContainer):

  def __init__(self, service):
    super(Screen, self).__init__()
    self._session_id = service.GetSessionId()
    self._screen_id = GenerateScreenId()

  def GetSessionId(self):
    return self._session_id
  def GetScreenId(self):
    return self._screen_id

  def AddMenu(self):
    return self.AddElement(MENU_ID, Menu())
  def GetMenu(self):
    return self.GetElement(MENU_ID)

  def AddMainButton(self, text=None, on_click=None, icon=None):
    return self.AddElement(MAIN_MENU_ID, Button(text=text, on_click=on_click, icon=icon))
  def GetMainButton(self):
    return self.GetElement(MAIN_MENU_ID)

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
     '_user_name': json_util.JSONString(),
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
    self._user_name = None
    self._datetime_added = datetime.datetime.now()

  def GetSessionId(self):
    return self._session_id
  def GetUserId(self):
    return self._session_id
  def IfSignedIn(self):
    return self._if_signed_in
  def GetUserName(self):
    return self._user_name

