from base_util import data_util
from base_util import json_util

import fase


@json_util.JSONDecorator({
    'device_type': json_util.JSONString(),
    'device_id': json_util.JSONString(),
    'device_token': json_util.JSONString(),
    'pixel_density': json_util.JSONFloat()})
class Device(data_util.AbstractObject):

  def __init__(self,
               device_type=None,
               device_id=None,
               device_token=None,
               pixel_density=None):
    self.device_type = device_type
    self.device_id = device_id
    self.device_token = device_token
    self.pixel_density = pixel_density


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


@json_util.JSONDecorator(
    {'version': json_util.JSONString()})
class VersionInfo(data_util.AbstractObject):

  def __init__(self,
               version=None):
    self.version = version


@json_util.JSONDecorator({
    'filename': json_util.JSONString()})
class Resource(data_util.AbstractObject):
  
  def __init__(self,
               filename=None):
    self.filename = filename


@json_util.JSONDecorator({
    'resource_list': json_util.JSONList(json_util.JSONObject(Resource)),
    'reset_resources': json_util.JSONBool()})
class Resources(data_util.AbstractObject):
  
  def __init__(self,
               resource_list=None,
               reset_resources=False):
    self.resource_list = resource_list or []
    self.reset_resources = reset_resources


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
    'method': json_util.JSONString(),
    'device': json_util.JSONObject(Device),
    'locale': json_util.JSONObject(fase.Locale)})
class ElementCallback(data_util.AbstractObject):

  def  __init__(self,
                elements_update=None,
                id_list=None,
                method=None,
                device=None,
                locale=None):
    self.elements_update = elements_update
    self.id_list = id_list
    self.method = method
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


@json_util.JSONDecorator(
    {'session_id': json_util.JSONString(),
     'service': json_util.JSONObject(fase.Service),
     'version': json_util.JSONString(),
     'device_list': json_util.JSONList(json_util.JSONObject(Device))})
class ServiceProg(data_util.AbstractObject):

  def __init__(self,
               session_id=None,
               service=None,
               version=None):
    self.session_id = session_id
    self.service = service
    self.version = version
    self.device_list = []


@json_util.JSONDecorator({
    'screen': json_util.JSONObject(fase.Screen),
    'resources': json_util.JSONObject(Resources),
    'elements_update': json_util.JSONObject(ElementsUpdate),
    'version_info': json_util.JSONObject(VersionInfo),
    'session_info': json_util.JSONObject(SessionInfo),
    'screen_info': json_util.JSONObject(ScreenInfo)})
class Response(data_util.AbstractObject):
  
  def __init__(self,
               screen=None,
               resources=None,
               elements_update=None,
               version_info=None,
               session_info=None,
               screen_info=None):
    self.screen = screen
    self.resources = resources
    self.elements_update = elements_update
    self.version_info = version_info
    self.session_info = session_info
    self.screen_info = screen_info


@json_util.JSONDecorator({
    'method': json_util.JSONString()})
class Method(data_util.AbstractObject):

  def __init__(self, method):
    self.method = method


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


def GetServiceProgScreenProg(device):
  assert fase.Service.service_cls is not None
  service_cls = fase.Service.service_cls
  latest_version = service_cls.Version()

  service = service_cls()
  screen = service.OnStart()
  service_prog = ServiceProg(session_id=service.GetSessionId(), service=service, version=latest_version)
  service_prog.device_list.append(device)
  screen_prog = ScreenProg(session_id=service.GetSessionId(), screen=screen, recent_device=device)
  return service_prog, screen_prog 


def SameDevice(device_1, device_2):
  return (device_1.device_type == device_2.device_type and device_1.device_id == device_2.device_id)


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
    element = element.GetElement(id_=id_)
  return element
