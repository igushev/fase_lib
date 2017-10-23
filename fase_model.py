import data_util
import json_util


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
    'user_id': json_util.JSONString(),
    'phone_number': json_util.JSONString(),
    'first_name': json_util.JSONString(),
    'last_name': json_util.JSONString(),
    'display_name': json_util.JSONString(),
    'device': json_util.JSONObject(Device),
    'datetime_added': json_util.JSONString()})
class User(data_util.AbstractObject):
  def __init__(self,
               user_id=None,
               phone_number=None,
               first_name=None,
               last_name=None,
               display_name=None,
               device=None,
               datetime_added=None):
    self.user_id = user_id
    self.phone_number = phone_number
    self.first_name = first_name
    self.last_name = last_name
    self.display_name = display_name
    self.device = device
    self.datetime_added = datetime_added


@json_util.JSONDecorator(
    {'id_to_value':
     json_util.JSONDict(json_util.JSONString(),
                        json_util.JSONString())},
    inherited=True)
class ScreenUpdate(data_util.AbstractObject):

  def __init__(self, id_to_value):
    self.id_to_value = id_to_value


@json_util.JSONDecorator(
    {'id_element': json_util.JSONString()})
class ElementClicked(data_util.AbstractObject):

  def  __init__(self,
                id_element,
                **kwargs):
    self.id_element = id_element


@json_util.JSONDecorator({
    'message': json_util.JSONString()})
class Status(data_util.AbstractObject):

  def __init__(self, message):
    self.message = message


class BadRequest(data_util.AbstractObject):

  def __init__(self, code, message):
    self.code = code
    self.message = message
