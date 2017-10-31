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
    {'id_list_list':
     json_util.JSONList(json_util.JSONList(json_util.JSONString())),
     'value_list': json_util.JSONList(json_util.JSONString())})
class ScreenUpdate(data_util.AbstractObject):

  def __init__(self,
               id_list_list=None,
               value_list=None):
    self.id_list_list = id_list_list
    self.value_list = value_list


@json_util.JSONDecorator(
    {'id_list':
     json_util.JSONList(json_util.JSONString())})
class ElementClicked(data_util.AbstractObject):

  def  __init__(self,
                id_list=None):
    self.id_list = id_list


@json_util.JSONDecorator({
    'screen': json_util.JSONObject(fase.Screen),
    'session_info': json_util.JSONObject(SessionInfo)})
class Response(data_util.AbstractObject):
  
  def __init__(self,
               screen=None,
               session_info=None,
               screen_info=None):
    self.screen = screen
    self.session_info = session_info
    self.screen_info = screen_info


@json_util.JSONDecorator({
    'message': json_util.JSONString()})
class Status(data_util.AbstractObject):

  def __init__(self, message):
    self.message = message


class BadRequest(data_util.AbstractObject):

  def __init__(self, code, message):
    self.code = code
    self.message = message
