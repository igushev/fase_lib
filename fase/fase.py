import datetime
import hashlib
import re
import uuid

from base_util import data_util
from base_util import json_util


DATETIME_FORMAT = json_util.DATETIME_FORMAT
DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'

MAIN_BUTTON_ID = 'main_button'
NAVIGATION_ID = 'navigation'
NEXT_STEP_BUTTON_ID = 'next_step_button'
PREV_STEP_BUTTON_ID = 'prev_step_button'
ALERT_ID = 'alert'
TITLE_IMAGE_ID = 'title_image'
CONTEXT_MENU_ID = 'context_menu'
IMAGE_ID = 'image'

ON_CLICK_METHOD = 'on_click'
ON_PICK_METHOD = 'on_pick'
ON_REFRESH_METHOD = 'on_refresh'
ON_MORE_METHOD = 'on_more'


def AssertIsInstanceOrNone(obj, expected_type):
  if obj is not None and not isinstance(obj, expected_type):
    raise AssertionError('Type must be %s or None, but type is %s, value is %s' % (expected_type, type(obj), obj))


def FunctionPlaceholder():
  pass


def GenerateElementId(element):
  return '%s_%s' % (element.__class__.__name__, str(uuid.uuid4()))


def GenerateSessionId():
  datetime_now = datetime.datetime.utcnow()
  session_id_hash = hashlib.md5()
  session_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH).encode('utf-8'))
  session_id = session_id_hash.hexdigest()
  return session_id


def GenerateScreenId(session_id):
  datetime_now = datetime.datetime.utcnow()
  screen_id_hash = hashlib.md5()
  screen_id_hash.update(session_id.encode('utf-8'))
  screen_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH).encode('utf-8'))
  screen_id = screen_id_hash.hexdigest()
  return screen_id


def GenerateUserId(session_id):
  datetime_now = datetime.datetime.utcnow()
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

  def GetCountryCode(self):
    return self.country_code


@json_util.JSONDecorator(
    {'display_name': json_util.JSONString(),
     'phone_number': json_util.JSONString()})
class Contact(data_util.AbstractObject):

  def __init__(self,
               display_name=None,
               phone_number=None):
    self.display_name = display_name
    self.phone_number = phone_number

  def Update(self, value):
    contact = Contact.FromJSON(value)
    self.__dict__ = contact.__dict__
  def Get(self):
    return self.ToJSON()

  def SetDisplayName(self, display_name):
    self.display_name = display_name
  def GetDisplayName(self):
    return self.display_name

  def SetPhoneNumber(self, phone_number):
    self.phone_number = phone_number
  def GetPhoneNumber(self):
    return self.phone_number


@json_util.JSONDecorator(
    {'date_of_birth': json_util.JSONBool(),
     'home_city': json_util.JSONBool(),
     'min_date_of_birth': json_util.JSONDateTime()})
class RequestUserData(data_util.AbstractObject):

  def __init__(self,
               date_of_birth=False,
               home_city=False,
               min_date_of_birth=None):
    self.date_of_birth = date_of_birth
    self.home_city = home_city
    self.min_date_of_birth = min_date_of_birth

  def GetDateOfBirth(self):
    return self.date_of_birth

  def GetHomeCity(self):
    return self.home_city


@json_util.JSONDecorator({
    'google_place_id': json_util.JSONString(),
    'city': json_util.JSONString(),
    'state': json_util.JSONString(),
    'country': json_util.JSONString()})
class Place(data_util.AbstractObject):

  def __init__(self,
               google_place_id=None,
               city=None,
               state=None,
               country=None):
    self.google_place_id = google_place_id
    self.city = city
    self.state = state
    self.country = country

  def Update(self, value):
    place = Place.FromJSON(value)
    self.__dict__ = place.__dict__
  def Get(self):
    return self.ToJSON()

  def GetGooglePlaceId(self):
    return self.google_place_id

  def GetCity(self):
    return self.city

  def GetState(self):
    return self.state

  def GetCountry(self):
    return self.country


@json_util.JSONDecorator({
    'user_id': json_util.JSONString(),
    'phone_number': json_util.JSONString(),
    'first_name': json_util.JSONString(),
    'last_name': json_util.JSONString(),
    'date_of_birth': json_util.JSONDateTime(),
    'home_city': json_util.JSONObject(Place),
    'locale': json_util.JSONObject(Locale),
    'datetime_added': json_util.JSONDateTime()})
class User(data_util.AbstractObject):
  def __init__(self,
               user_id=None,
               phone_number=None,
               first_name=None,
               last_name=None,
               date_of_birth=None,
               home_city=None,
               locale=None,
               datetime_added=None):
    self.user_id = user_id
    self.phone_number = phone_number
    self.first_name = first_name
    self.last_name = last_name
    self.date_of_birth = date_of_birth
    self.home_city = home_city
    self.locale = locale 
    self.datetime_added = datetime_added

  def GetPhoneNumber(self):
    return self.phone_number

  def GetFirstName(self):
    return self.first_name

  def GetLastName(self):
    return self.last_name

  def GetDateOfBirth(self):
    return self.date_of_birth

  def GetHomeCity(self):
    return self.home_city

  def GetLocale(self):
    return self.locale

  def DisplayName(self):
    if self.first_name and self.last_name:
      return ' '.join([self.first_name, self.last_name])
    elif self.first_name:
      return self.first_name
    elif self.last_name:
      return self.last_name
    else:
      return self.phone_number


@json_util.JSONDecorator({
    'device_type': json_util.JSONString(),
    'device_token': json_util.JSONString(),
    'pixel_density': json_util.JSONFloat()})
class Device(data_util.AbstractObject):

  def __init__(self,
               device_type=None,
               device_token=None,
               pixel_density=None):
    self.device_type = device_type
    self.device_token = device_token
    self.pixel_density = pixel_density


@json_util.JSONDecorator({}, inherited=True)
class Element(data_util.AbstractObject):
  """Basic Interface."""
  def __init__(self):
    super(Element, self).__init__()

  def CallCallback(self, service, screen, device, method):
    screen = getattr(self, method)(service, screen, self)
    return service, screen


@json_util.JSONDecorator(
    {'id_element_list': json_util.JSONList(json_util.JSONTuple([json_util.JSONString(),
                                                                json_util.JSONObject(Element)]))})
class ElementContainer(Element):
  """Basic Interface which contains list if id and Element pairs."""
  def __init__(self):
    super(ElementContainer, self).__init__()
    self.id_element_list = []

  def AddElement(self, *, id_=None, element):
    if id_ is None:
      id_ = GenerateElementId(element)
    assert not self.HasElement(id_=id_)
    self.id_element_list.append((id_, element))
    return element

  def HasElement(self, *, id_):
    for id_in_list, _ in self.id_element_list:
      if id_in_list == id_:
        return True
    return False

  def GetElement(self, *, id_):
    for id_in_list, value in self.id_element_list:
      if id_in_list == id_:
        return value
    raise KeyError(id_)

  def PopElement(self, *, id_):
    for i, (id_in_list, value) in enumerate(self.id_element_list):
      if id_in_list == id_:
        del self.id_element_list[i]
        return value
    raise KeyError(id_)

  def GetIdElementList(self):
    return self.id_element_list


@json_util.JSONDecorator({})
class Variable(Element):
  def __init__(self):
    super(Variable, self).__init__()


@json_util.JSONDecorator(
    {'value': json_util.JSONInt()})
class IntVariable(Variable):
  def __init__(self, value):
    super(IntVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    AssertIsInstanceOrNone(value, int)
    self.value = value
  def GetValue(self):
    return self.value


@json_util.JSONDecorator(
    {'value': json_util.JSONFloat()})
class FloatVariable(Variable):
  def __init__(self, value):
    super(FloatVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    AssertIsInstanceOrNone(value, float)
    self.value = value
  def GetValue(self):
    return self.value


@json_util.JSONDecorator(
    {'value': json_util.JSONString()})
class StringVariable(Variable):
  def __init__(self, value):
    super(StringVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    AssertIsInstanceOrNone(value, str)
    self.value = value
  def GetValue(self):
    return self.value


@json_util.JSONDecorator(
    {'value': json_util.JSONBool()})
class BoolVariable(Variable):
  def __init__(self, value):
    super(BoolVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    AssertIsInstanceOrNone(value, bool)
    self.value = value
  def GetValue(self):
    return self.value


@json_util.JSONDecorator(
    {'value': json_util.JSONDateTime()})
class DateTimeVariable(Variable):
  def __init__(self, value):
    super(DateTimeVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    AssertIsInstanceOrNone(value, datetime.datetime)
    self.value = value
  def GetValue(self):
    return self.value


@json_util.JSONDecorator(
    {'value': json_util.JSONFunction()})
class FunctionVariable(Variable):
  def __init__(self, value):
    super(FunctionVariable, self).__init__()
    self.SetValue(value)

  def SetValue(self, value):
    assert callable(value)
    self.value = value
  def GetValue(self):
    return self.value


@json_util.JSONDecorator({})
class VariableContainer(ElementContainer):
  def __init__(self):
    super(VariableContainer, self).__init__()

  def AddIntVariable(self, *, id_, value):
    return self.AddElement(id_=id_, element=IntVariable(value))
  def HasIntVariable(self, *, id_):
    return self.HasElement(id_=id_)
  def GetIntVariable(self, *, id_):
    return self.GetElement(id_=id_)
  def PopIntVariable(self, *, id_):
    return self.PopElement(id_=id_)

  def AddFloatVariable(self, *, id_, value):
    return self.AddElement(id_=id_, element=FloatVariable(value))
  def HasFloatVariable(self, *, id_):
    return self.HasElement(id_=id_)
  def GetFloatVariable(self, *, id_):
    return self.GetElement(id_=id_)
  def PopFloatVariable(self, *, id_):
    return self.PopElement(id_=id_)

  def AddStringVariable(self, *, id_, value):
    return self.AddElement(id_=id_, element=StringVariable(value))
  def HasStringVariable(self, *, id_):
    return self.HasElement(id_=id_)
  def GetStringVariable(self, *, id_):
    return self.GetElement(id_=id_)
  def PopStringVariable(self, *, id_):
    return self.PopElement(id_=id_)

  def AddBoolVariable(self, *, id_, value):
    return self.AddElement(id_=id_, element=BoolVariable(value))
  def HasBoolVariable(self, *, id_):
    return self.HasElement(id_=id_)
  def GetBoolVariable(self, *, id_):
    return self.GetElement(id_=id_)
  def PopBoolVariable(self, *, id_):
    return self.PopElement(id_=id_)

  def AddDateTimeVariable(self, *, id_, value):
    return self.AddElement(id_=id_, element=DateTimeVariable(value))
  def HasDateTimeVariable(self, *, id_):
    return self.HasElement(id_=id_)
  def GetDateTimeVariable(self, *, id_):
    return self.GetElement(id_=id_)
  def PopDateTimeVariable(self, *, id_):
    return self.PopElement(id_=id_)

  def AddFunctionVariable(self, *, id_, value):
    return self.AddElement(id_=id_, element=FunctionVariable(value))
  def HasFunctionVariable(self, *, id_):
    return self.HasElement(id_=id_)
  def GetFunctionVariable(self, *, id_):
    return self.GetElement(id_=id_)
  def PopFunctionVariable(self, *, id_):
    return self.PopElement(id_=id_)


@json_util.JSONDecorator(
    {'displayed': json_util.JSONBool(),
     'request_locale': json_util.JSONBool(),
     'locale': json_util.JSONObject(Locale)})
class VisualElement(VariableContainer):
  """Basic Interface for Visual Elements."""
  def __init__(self):
    super(VisualElement, self).__init__()
    self.displayed = True
    self.request_locale = False
    self.locale = None

  def SetDisplayed(self, displayed):
    self.displayed = displayed
  def GetDisplayed(self):
    return self.displayed

  def SetRequestLocale(self, request_locale):
    self.request_locale = request_locale
  def GetRequestLocale(self):
    return self.request_locale
  def SetLocale(self, locale):
    self.locale = locale
  def GetLocale(self):
    return self.locale


@json_util.JSONDecorator(
    {'text': json_util.JSONString(),
     'font': json_util.JSONFloat(),
     'size': json_util.JSONInt(),
     'align': json_util.JSONInt(),
     'on_click': json_util.JSONFunction()})
class Label(VisualElement):

  FONT_LIST = [0.5, 0.75, 1., 1.25, 1.5]

  MIN = 1
  MAX = 2

  LEFT = 1
  RIGHT = 2
  CENTER = 3

  def __init__(self,
               text=None,
               font=None,
               size=None,
               align=None,
               on_click=None):
    super(Label, self).__init__()
    self.text = text  # Can be None
    self.font = font or 1.
    assert self.font in Label.FONT_LIST
    self.size = size or Label.MIN
    self.align = align or Label.CENTER
    self.on_click = on_click

  def GetText(self):
    return self.text

  def GetFont(self):
    return self.font

  def GetSize(self):
    return self.size

  def GetAlign(self):
    return self.align

  def GetOnClick(self):
    return self.on_click


@json_util.JSONDecorator(
    {'text': json_util.JSONString(),
     'hint': json_util.JSONString(),
     'size': json_util.JSONInt(),
     'type': json_util.JSONInt(),
     'multiline': json_util.JSONBool()})
class Text(VisualElement):

  MIN = 1
  MAX = 2

  TEXT = 1
  DIGITS = 2
  PHONE = 3
  EMAIL = 4

  def __init__(self,
               text=None,
               hint=None,
               size=None,
               type_=None,
               multiline=None):
    super(Text, self).__init__()
    self.text = text or ''
    self.hint = hint  # Can be None
    self.size = size or Text.MIN
    self.type = type_ or Text.TEXT
    self.multiline = multiline or False

  def Update(self, value):
    self.text = value
  def Get(self):
    return self.text

  def SetText(self, text):
    self.text = text
  def GetText(self):
    return self.text

  def GetHint(self):
    return self.hint

  def GetSize(self):
    return self.size

  def GetType(self):
    return self.type


@json_util.JSONDecorator(
    {'value': json_util.JSONBool(),
     'text': json_util.JSONString(),
     'align': json_util.JSONInt()})
class Switch(VisualElement):

  LEFT = 1
  RIGHT = 2
  CENTER = 3
  
  def __init__(self,
               value=None,
               text=None,
               align=None):
    super(Switch, self).__init__()
    assert value is not None
    self.value = value
    self.text = text  # Can be None
    self.align = align or Switch.CENTER

  def Update(self, value):
    self.value = (value == str(True))
  def Get(self):
    return str(self.value)

  def SetValue(self, value):
    self.value = value
  def GetValue(self):
    return self.value

  def GetText(self):
    return self.text

  def GetAlign(self):
    return self.align


@json_util.JSONDecorator(
    {'value': json_util.JSONString(),
     'items': json_util.JSONList(json_util.JSONString()),
     'hint': json_util.JSONString(),
     'align': json_util.JSONInt()})
class Select(VisualElement):

  LEFT = 1
  RIGHT = 2
  CENTER = 3
  
  def __init__(self,
               value=None,
               items=None,
               hint=None,
               align=None):
    super(Select, self).__init__()
    self.value = value  # Can be None, since should be entered
    assert len(items) > 0
    self.items = items
    self.hint = hint  # Can be None
    self.align = align or Select.CENTER

  def Update(self, value):
    self.value = value
  def Get(self):
    return self.value

  def SetValue(self, value):
    self.value = value
  def GetValue(self):
    return self.value

  def GetItems(self):
    return self.items

  def GetHint(self):
    return self.hint

  def GetAlign(self):
    return self.align


@json_util.JSONDecorator(
    {'value': json_util.JSONFloat(),
     'min_value': json_util.JSONFloat(),
     'max_value': json_util.JSONFloat(),
     'step': json_util.JSONFloat()})
class Slider(VisualElement):

  def __init__(self,
               value=None,
               min_value=None,
               max_value=None,
               step=None):
    super(Slider, self).__init__()
    assert value is not None
    self.value = value
    assert min_value is not None
    self.min_value = min_value
    assert max_value is not None
    self.max_value = max_value
    self.step = step  # Can be None

  def Update(self, value):
    self.value = float(value)
  def Get(self):
    return str(self.value)

  def GetValue(self):
    return self.value

  def GetMinValue(self):
    return self.min_value

  def GetMaxValue(self):
    return self.max_value

  def GetStep(self):
    return self.step


@json_util.JSONDecorator({
    'filename': json_util.JSONString(),
    'url': json_util.JSONString()})
class Image(VisualElement):
  def __init__(self,
               filename=None,
               url=None):
    super(Image, self).__init__()
    assert filename or url
    self.filename = filename
    self.url = url

  def SetFilename(self, filename):
    self.filename = filename
  def GetFilename(self):
    return self.filename

  def GetUrl(self):
    return self.url


@json_util.JSONDecorator(
    {'text': json_util.JSONString(),
     'on_click': json_util.JSONFunction()})
class MenuItem(VisualElement):

  def __init__(self,
               text=None,
               image=None,
               on_click=None):
    super(MenuItem, self).__init__()
    assert text or image
    self.text = text
    if image:
      self.AddImage(image)
    self.on_click = on_click

  def SetText(self, text):
    self.text = text
  def GetText(self):
    return self.text

  def AddImage(self, image):
    return self.AddElement(id_=IMAGE_ID, element=image)
  def HasImage(self):
    return self.HasElement(id_=IMAGE_ID)
  def GetImage(self):
    return self.GetElement(id_=IMAGE_ID)

  def GetOnClick(self):
    return self.on_click


@json_util.JSONDecorator({
    'text': json_util.JSONString()})
class Menu(ElementContainer):
  def __init__(self, text=None):
    super(Menu, self).__init__()
    self.text = text

  def GetText(self):
    return self.text

  def AddMenuItem(self, *,
                  id_=None,
                  text=None,
                  image=None,
                  on_click=None):
    return self.AddElement(id_=id_, element=MenuItem(text=text,
                                                     image=image,
                                                     on_click=on_click))
  def HasMenuItem(self, *, id_):
    return self.HasElement(id_=id_)
  def GetMenuItem(self, *, id_):
    return self.GetElement(id_=id_)


@json_util.JSONDecorator(
    {'text': json_util.JSONString(),
     'on_click': json_util.JSONFunction()})
class Button(VisualElement):

  def __init__(self,
               text=None,
               image=None,
               on_click=None):
    super(Button, self).__init__()
    assert text or image
    self.text = text
    if image:
      self.AddImage(image)
    self.on_click = on_click

  def SetText(self, text):
    self.text = text
  def GetText(self):
    return self.text

  def AddImage(self, image):
    return self.AddElement(id_=IMAGE_ID, element=image)
  def HasImage(self):
    return self.HasElement(id_=IMAGE_ID)
  def GetImage(self):
    return self.GetElement(id_=IMAGE_ID)

  def GetOnClick(self):
    return self.on_click

  def AddContextMenu(self, text=None):
    return self.AddElement(id_=CONTEXT_MENU_ID, element=Menu(text=text))
  def HasContextMenu(self):
    return self.HasElement(id_=CONTEXT_MENU_ID)
  def GetContextMenu(self):
    return self.GetElement(id_=CONTEXT_MENU_ID)


@json_util.JSONDecorator({})
class Navigation(ElementContainer):
  def __init__(self):
    super(Navigation, self).__init__()

  def AddButton(self, *,
                id_=None,
                text=None,
                image=None,
                on_click=None):
    return self.AddElement(id_=id_, element=Button(text=text,
                                                   image=image,
                                                   on_click=on_click))
  def HasButton(self, *, id_):
    return self.HasElement(id_=id_)
  def GetButton(self, *, id_):
    return self.GetElement(id_=id_)
    

@json_util.JSONDecorator(
    {'contact': json_util.JSONObject(Contact),
     'hint': json_util.JSONString(),
     'size': json_util.JSONInt(),
     'on_pick': json_util.JSONFunction()})
class ContactPicker(VisualElement):

  MIN = 1
  MAX = 2
  
  def __init__(self,
               contact=None,
               hint=None,
               size=None,
               on_pick=None):
    super(ContactPicker, self).__init__()
    self.contact = contact  # Can be None, since should be entered
    self.hint = hint  # Can be None
    self.size = size or ContactPicker.MIN
    self.on_pick = on_pick

  def Update(self, value):
    if not value:
      self.contact = None
      return
    if self.contact is None:
      self.contact = Contact()
    self.contact.Update(value)
  def Get(self):
    return self.contact.Get() if self.contact is not None else None

  def GetContact(self):
    return self.contact

  def GetHint(self):
    return self.hint

  def GetSize(self):
    return self.size

  def GetOnPick(self):
    return self.on_pick


@json_util.JSONDecorator(
    {'datetime': json_util.JSONDateTime(),
     'type': json_util.JSONInt(),
     'hint': json_util.JSONString(),
     'size': json_util.JSONInt()})
class DateTimePicker(VisualElement):

  DATE = 1
  TIME = 2
  DATETIME = 3

  MIN = 1
  MAX = 2
  
  def __init__(self,
               datetime_=None,
               type_=None,
               hint=None,
               size=None):
    super(DateTimePicker, self).__init__()
    self.datetime = datetime_  # Can be None, since should be entered
    self.type = type_ or DateTimePicker.DATETIME
    self.hint = hint  # Can be None
    self.size = size or DateTimePicker.MIN

  def Update(self, value):
    self.datetime = datetime.datetime.strptime(value, DATETIME_FORMAT) if value else None

  def Get(self):
    return self.datetime.strftime(DATETIME_FORMAT) if self.datetime is not None else None

  def GetDateTime(self):
    return self.datetime

  def GetType(self):
    return self.type

  def GetHint(self):
    return self.hint

  def GetSize(self):
    return self.size


@json_util.JSONDecorator(
    {'place': json_util.JSONObject(Place),
     'type': json_util.JSONInt(),
     'hint': json_util.JSONString(),
     'size': json_util.JSONInt()})
class PlacePicker(VisualElement):

  CITY = 1

  MIN = 1
  MAX = 2
  
  def __init__(self,
               place=None,
               type_=None,
               hint=None,
               size=None):
    super(PlacePicker, self).__init__()
    self.place = place  # Can be None, since should be entered
    assert type_ is not None
    self.type = type_
    self.hint = hint  # Can be None
    self.size = size or PlacePicker.MIN
    
  def Update(self, value):
    if not value:
      self.place = None
      return
    if self.place is None:
      self.place = Place()
    self.place.Update(value)
  def Get(self):
    return self.place.Get() if self.place is not None else None

  def GetPlace(self):
    return self.place

  def GetType(self):
    return self.type

  def GetHint(self):
    return self.hint

  def GetSize(self):
    return self.size


@json_util.JSONDecorator({})
class Separator(VisualElement):

  def __init__(self):
    super(Separator, self).__init__()


@json_util.JSONDecorator(
    {'url': json_util.JSONString(),
     'size': json_util.JSONInt(),
     'scrollable': json_util.JSONBool()})
class Web(VisualElement):

  MIN = 1
  MAX = 2

  def __init__(self,
               url=None,
               size=None,
               scrollable=None):
    super(Web, self).__init__()
    assert url is not None
    self.url = url
    self.size = size or Web.MIN
    self.scrollable = scrollable or True

  def GetUrl(self):
    return self.url

  def GetSize(self):
    return self.size

  def GetScrollable(self):
    return self.scrollable


@json_util.JSONDecorator({})
class BaseElementsContainer(VisualElement):
  def __init__(self):
    super(BaseElementsContainer, self).__init__()

  def AddFrame(self, *,
               id_=None,
               orientation=None,
               size=None,
               border=None,
               on_click=None):
    return self.AddElement(id_=id_, element=Frame(orientation=orientation, size=size, border=border, on_click=on_click))
  def HasFrame(self, *, id_):
    return self.HasElement(id_=id_)
  def GetFrame(self, *, id_):
    return self.GetElement(id_=id_)

  def AddLabel(self, *,
               id_=None,
               text=None,
               font=None,
               size=None,
               align=None):
    return self.AddElement(id_=id_, element=Label(text=text, font=font, size=size, align=align))
  def HasLabel(self, *, id_):
    return self.HasElement(id_=id_)
  def GetLabel(self, *, id_):
    return self.GetElement(id_=id_)

  def AddText(self, *,
              id_=None,
              text=None,
              hint=None,
              size=None,
              type_=None,
              multiline=None):
    return self.AddElement(id_=id_, element=Text(text=text, hint=hint, size=size, type_=type_, multiline=multiline))
  def HasText(self, *, id_):
    return self.HasElement(id_=id_)
  def GetText(self, *, id_):
    return self.GetElement(id_=id_)

  def AddSwitch(self, *,
                id_=None,
                value=None,
                text=None,
                align=None):
    return self.AddElement(id_=id_, element=Switch(value=value, text=text, align=align))
  def HasSwitch(self, *, id_):
    return self.HasElement(id_=id_)
  def GetSwitch(self, *, id_):
    return self.GetElement(id_=id_)

  def AddSelect(self, *,
                id_=None,
                value=None,
                items=None,
                hint=None,
                align=None):
    return self.AddElement(id_=id_, element=Select(value=value, items=items, hint=hint, align=align))
  def HasSelect(self, *, id_):
    return self.HasElement(id_=id_)
  def GetSelect(self, *, id_):
    return self.GetElement(id_=id_)

  def AddImage(self, *,
               id_=None,
               filename=None,
               url=None):
    return self.AddElement(id_=id_, element=Image(filename=filename, url=url))
  def HasImage(self, *, id_):
    return self.HasElement(id_=id_)
  def GetImage(self, *, id_):
    return self.GetElement(id_=id_)

  def AddSlider(self, *,
                id_=None,
                value=None,
                min_value=None,
                max_value=None,
                step=None):
    return self.AddElement(id_=id_, element=Slider(value=value, min_value=min_value, max_value=max_value, step=step))
  def HasSlider(self, *, id_):
    return self.HasElement(id_=id_)
  def GetSlider(self, *, id_):
    return self.GetElement(id_=id_)

  def AddButton(self, *,
                id_=None,
                text=None,
                image=None,
                on_click=None):
    return self.AddElement(id_=id_, element=Button(text=text, on_click=on_click, image=image))
  def HasButton(self, *, id_):
    return self.HasElement(id_=id_)
  def GetButton(self, *, id_):
    return self.GetElement(id_=id_)

  def AddContactPicker(self, *,
                       id_=None,
                       contact=None,
                       hint=None,
                       size=None,
                       on_pick=None):
    return self.AddElement(id_=id_, element=ContactPicker(contact=contact, hint=hint, size=size, on_pick=on_pick))
  def HasContactPicker(self, *, id_):
    return self.HasElement(id_=id_)
  def GetContactPicker(self, *, id_):
    return self.GetElement(id_=id_)

  def AddDateTimePicker(self, *,
                        id_=None,
                        datetime_=None,
                        type_=None,
                        hint=None,
                        size=None):
    return self.AddElement(id_=id_, element=DateTimePicker(datetime_=datetime_, type_=type_, hint=hint, size=size))
  def HasDateTimePicker(self, *, id_):
    return self.HasElement(id_=id_)
  def GetDateTimePicker(self, *, id_):
    return self.GetElement(id_=id_)

  def AddPlacePicker(self, *,
                     id_=None,
                     place=None,
                     type_=None,
                     hint=None,
                     size=None):
    return self.AddElement(id_=id_, element=PlacePicker(place=place, type_=type_, hint=hint, size=size))
  def HasPlacePicker(self, *, id_):
    return self.HasElement(id_=id_)
  def GetPlacePicker(self, *, id_):
    return self.GetElement(id_=id_)

  def AddSeparator(self, *,
                   id_=None):
    return self.AddElement(id_=id_, element=Separator())
  def HasSeparator(self, *, id_):
    return self.HasElement(id_=id_)
  def GetSeparator(self, *, id_):
    return self.GetElement(id_=id_)

  def AddWeb(self, *,
             id_=None,
             url=None,
             size=None,
             scrollable=None):
    return self.AddElement(id_=id_, element=Web(url=url, size=size, scrollable=scrollable))
  def HasWeb(self, *, id_):
    return self.HasElement(id_=id_)
  def GetWeb(self, *, id_):
    return self.GetElement(id_=id_)


@json_util.JSONDecorator(
    {'orientation': json_util.JSONInt(),
     'size': json_util.JSONInt(),
     'on_click': json_util.JSONFunction(),
     'border': json_util.JSONBool()})
class Frame(BaseElementsContainer):

  VERTICAL = 1
  HORIZONTAL = 2

  MIN = 1
  MAX = 2

  def __init__(self,
               orientation=None,
               size=None,
               border=None,
               on_click=None):
    super(Frame, self).__init__()
    self.orientation = orientation or Frame.VERTICAL
    self.size = size or Frame.MIN
    self.border = border  # Can be None
    self.on_click = on_click

  def GetOrientation(self):
    return self.orientation

  def GetSize(self):
    return self.size

  def GetOnClick(self):
    return self.on_click

  def GetBorder(self):
    return self.border


@json_util.JSONDecorator(
    {'text': json_util.JSONString()})
class Alert(ElementContainer):

  def __init__(self, text=None):
    super(Alert, self).__init__()
    assert text is not None
    self.text = text

  def GetText(self):
    return self.text

  def AddButton(self, *,
                id_=None,
                text=None,
                image=None,
                on_click=None):
    return self.AddElement(id_=id_, element=Button(text=text,
                                                   image=image,
                                                   on_click=on_click))
  def HasButton(self, *, id_):
    return self.HasElement(id_=id_)
  def GetButton(self, *, id_):
    return self.GetElement(id_=id_)


@json_util.JSONDecorator(
    {'_screen_id': json_util.JSONString(),
     'scrollable': json_util.JSONBool(),
     'title': json_util.JSONString(),
     'on_refresh': json_util.JSONFunction(),
     'on_more': json_util.JSONFunction()})
class Screen(BaseElementsContainer):

  def __init__(self, service):
    super(Screen, self).__init__()
    self._screen_id = GenerateScreenId(service.GetSessionId())
    self.scrollable = None
    self.title = None
    self.on_refresh = None
    self.on_more = None

  def UpdateScreenId(self, service):
    self._screen_id = GenerateScreenId(service.GetSessionId())
  def GetScreenId(self):
    return self._screen_id

  def SetScrollable(self, scrollable):
    self.scrollable = scrollable
  def GetScrollable(self):
    return self.scrollable

  def SetTitle(self, title):
    assert not self.HasTitleImage()
    self.title = title
  def GetTitle(self):
    return self.title

  def AddTitleImage(self, title_image):
    assert self.title is None
    return self.AddElement(id_=TITLE_IMAGE_ID, element=title_image)
  def HasTitleImage(self):
    return self.HasElement(id_=TITLE_IMAGE_ID)
  def GetTitleImage(self):
    return self.GetElement(id_=TITLE_IMAGE_ID)

  def SetOnRefresh(self, on_refresh):
    self.on_refresh = on_refresh
  def GetOnRefresh(self):
    return self.on_refresh

  def SetOnMore(self, on_more):
    self.on_more = on_more
  def GetOnMore(self):
    return self.on_more

  def AddMainButton(self, text=None, image=None, on_click=None):
    return self.AddElement(id_=MAIN_BUTTON_ID, element=Button(text=text, image=image, on_click=on_click))
  def HasMainButton(self):
    return self.HasElement(id_=MAIN_BUTTON_ID)
  def GetMainButton(self):
    return self.GetElement(id_=MAIN_BUTTON_ID)

  def AddNavigation(self):
    return self.AddElement(id_=NAVIGATION_ID, element=Navigation())
  def HasNavigation(self):
    return self.HasElement(id_=NAVIGATION_ID)
  def GetNavigation(self):
    return self.GetElement(id_=NAVIGATION_ID)

  def AddNextStepButton(self, text=None, image=None, on_click=None):
    return self.AddElement(id_=NEXT_STEP_BUTTON_ID, element=Button(text=text, image=image, on_click=on_click))
  def HasNextStepButton(self):
    return self.HasElement(id_=NEXT_STEP_BUTTON_ID)
  def GetNextStepButton(self):
    return self.GetElement(id_=NEXT_STEP_BUTTON_ID)

  def AddPrevStepButton(self, text=None, image=None, on_click=None):
    return self.AddElement(id_=PREV_STEP_BUTTON_ID, element=Button(text=text, image=image, on_click=on_click))
  def HasPrevStepButton(self):
    return self.HasElement(id_=PREV_STEP_BUTTON_ID)
  def GetPrevStepButton(self):
    return self.GetElement(id_=PREV_STEP_BUTTON_ID)

  def AddAlert(self, text=None):
    return self.AddElement(id_=ALERT_ID, element=Alert(text=text))
  def HasAlert(self):
    return self.HasElement(id_=ALERT_ID)
  def GetAlert(self):
    return self.GetElement(id_=ALERT_ID) 


@json_util.JSONDecorator(
    {'_session_id': json_util.JSONString(),
     '_if_signed_in': json_util.JSONBool(),
     '_user_id': json_util.JSONString(),
     '_user': json_util.JSONObject(User),
     '_device_list': json_util.JSONList(json_util.JSONObject(Device)),
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
    self._user = None
    self._device_list = []
    self._datetime_added = datetime.datetime.utcnow().replace(microsecond=0)

  def GetSessionId(self):
    return self._session_id
  def IfSignedIn(self):
    return self._if_signed_in
  def GetUserId(self):
    return self._user_id
  def GetUser(self):
    return self._user
