import data_util
import json_util

import fase


@json_util.JSONDecorator({
    'device_type': json_util.JSONString(),
    'device_token': json_util.JSONString()})
class Device(data_util.AbstractObject):

  def __init__(self,
               device_type=None,
               device_token=None):
    self.device_type = device_type
    self.device_token = device_token


@json_util.JSONDecorator({
    'session_id': json_util.JSONString()})
class SessionInfo(data_util.AbstractObject):

  def __init__(self,
               session_id=None):
    self.session_id = session_id


@json_util.JSONDecorator({
    'screen_id': json_util.JSONString()})
class ScreenInfo(data_util.AbstractObject):

  def __init__(self,
               screen_id=None):
    self.screen_id = screen_id


@json_util.JSONDecorator({
    'user_id': json_util.JSONString(),
    'phone_number': json_util.JSONString(),
    'first_name': json_util.JSONString(),
    'last_name': json_util.JSONString(),
    'datetime_added': json_util.JSONDateTime()})
class User(data_util.AbstractObject):
  def __init__(self,
               user_id=None,
               phone_number=None,
               first_name=None,
               last_name=None,
               datetime_added=None):
    self.user_id = user_id
    self.phone_number = phone_number
    self.first_name = first_name
    self.last_name = last_name
    self.datetime_added = datetime_added

  def PhoneNumber(self):
    return self.phone_number

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
    'id_list_list': json_util.JSONList(json_util.JSONList(json_util.JSONString())),
    'value_list': json_util.JSONList(json_util.JSONString())})
class ElementsUpdate(data_util.AbstractObject):

  def __init__(self,
               id_list_list=None,
               value_list=None):
    self.id_list_list = id_list_list
    self.value_list = value_list


@json_util.JSONDecorator({
    'elements_update': json_util.JSONObject(ElementsUpdate),
    'device': json_util.JSONObject(Device)})
class ScreenUpdate(data_util.AbstractObject):

  def  __init__(self,
                elements_update=None,
                device=None):
    self.elements_update = elements_update
    self.device = device


@json_util.JSONDecorator({
    'elements_update': json_util.JSONObject(ElementsUpdate),
    'id_list': json_util.JSONList(json_util.JSONString()),
    'device': json_util.JSONObject(Device),
    'locale': json_util.JSONObject(fase.Locale)})
class ElementClicked(data_util.AbstractObject):

  def  __init__(self,
                elements_update=None,
                id_list=None,
                device=None,
                locale=None):
    self.elements_update = elements_update
    self.id_list = id_list
    self.device = device
    self.locale = locale


@json_util.JSONDecorator({
    'session_id': json_util.JSONString(),
    'screen': json_util.JSONObject(fase.Screen),
    'elements_update': json_util.JSONObject(ElementsUpdate),
    'recent_device': json_util.JSONObject(Device)})
class ScreenProg(data_util.AbstractObject):

  def __init__(self,
               session_id=None,
               screen=None,
               elements_update=None,
               recent_device=None):
    self.session_id = session_id
    self.screen = screen
    self.elements_update = elements_update
    self.recent_device = recent_device


@json_util.JSONDecorator({
    'screen': json_util.JSONObject(fase.Screen),
    'elements_update': json_util.JSONObject(ElementsUpdate),
    'session_info': json_util.JSONObject(SessionInfo),
    'screen_info': json_util.JSONObject(ScreenInfo)})
class Response(data_util.AbstractObject):
  
  def __init__(self,
               screen=None,
               elements_update=None,
               session_info=None,
               screen_info=None):
    self.screen = screen
    self.elements_update = elements_update
    self.session_info = session_info
    self.screen_info = screen_info


@json_util.JSONDecorator({
    'command': json_util.JSONString()})
class Command(data_util.AbstractObject):

  def __init__(self, command):
    self.command = command


@json_util.JSONDecorator({
    'message': json_util.JSONString()})
class Status(data_util.AbstractObject):

  def __init__(self, message):
    self.message = message


@json_util.JSONDecorator({
    'code': json_util.JSONInt(),
    'message': json_util.JSONString()})
class BadRequest(data_util.AbstractObject):

  def __init__(self, code, message):
    self.code = code
    self.message = message


def ElementsUpdateToDict(elements_update):
  return {tuple(id_list): value for id_list, value in zip(elements_update.id_list_list, elements_update.value_list)}


def DictToElementsUpdate(id_list_to_value):
  if not id_list_to_value:
    return None
  id_list_list = []
  value_list = []
  for id_list, value in id_list_to_value.items():
    id_list_list.append(list(id_list))
    value_list.append(value)
  return ElementsUpdate(id_list_list=id_list_list, value_list=value_list)


def GetScreenElement(screen, id_list):
  element = screen
  for id_ in id_list:
    element = element.GetElement(id_)
  return element
