from collections import namedtuple
import hyper
import json
import jwt
import requests
import time

from fase_lib.base_util import singleton_util


IOS = 'iOS'
IOS_JWT_ALGORITHM = 'ES256'
IOS_SOUND = 'default'
IOS_HTTP_METHOD = 'POST'

ANDROID = 'Android'
ANDROID_SOUND = 'default'

UPDATE_THROW_ERROR = 'Include text to throw update error'
DELETE_THROW_ERROR = 'Include text to throw delete error'
PUSH_THROW_ERROR = 'Include text to throw push error'
Notification = namedtuple('Notification', ['device_token', 'title', 'message'])


class UnknownDeviceTypeException(Exception):
  pass


class UpdateDeviceTokenException(Exception):
  
  def __init__(self, device_token):
    self.device_token = device_token


class DeleteSessionException(Exception):
  pass


class PushNotificationException(Exception):
  pass


class DevicePushServiceProviderInterface(object):

  def Push(self, device, message):
    raise NotImplemented()


class iOSDevicePushServiceProvider(DevicePushServiceProviderInterface):
  
  def __init__(self, server_url, key_id, team_id, key_file, app_id):
    self.server_url = server_url
    self.key_id = key_id
    self.team_id = team_id
    self.key_file = key_file
    self.app_id = app_id
    self.key = open(self.key_file).read() 

  def Push(self, device_token, title, message):
    path = '/3/device/%s' % device_token
    token = jwt.encode({'iss': self.team_id,
                        'iat': int(time.time())},
                       self.key,
                       algorithm=IOS_JWT_ALGORITHM,
                       headers={'alg': IOS_JWT_ALGORITHM,
                                'kid': self.key_id})    
    
    headers={'authorization': 'bearer %s' % token.decode('ascii'),
             'apns-topic': self.app_id}
    
    payload = {'aps': {'alert': {'title': title,
                                 'body': message},
                       'sound': IOS_SOUND}}
    http_connection = hyper.HTTPConnection(self.server_url)
    http_connection.request(IOS_HTTP_METHOD, path, body=json.dumps(payload).encode('utf-8'), headers=headers)
    http_response = http_connection.get_response()
    if http_response.status == 410:
      raise DeleteSessionException()
    if http_response.status != 200:
      raise PushNotificationException(http_response.read())


class AndroidDevicePushServiceProvider(DevicePushServiceProviderInterface):

  def __init__(self, server_url, app_id):
    self.server_url = server_url
    self.app_id = app_id

  def Push(self, device_token, title, message):
    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : 'key=%s' % self.app_id}
    data = { 
      'to' : device_token,
      'notification' : {
          'title' : title,
          'body' : message,
          'sound': ANDROID_SOUND,
          'icon' : 'myicon'}
    }

    http_response = requests.post(self.server_url, headers=headers, json=data)
    if http_response.status_code != 200:
      raise PushNotificationException(http_response.text)
    result = http_response.json()
    if not result['failure'] and not result['canonical_ids']:
      return
    assert len(result['results']) == 1
    single_result = next(iter(result['results']))
    if 'message_id' in single_result and 'registration_id' in single_result:
      raise UpdateDeviceTokenException(single_result['registration_id'])
    if 'error' in single_result and single_result['error'] == 'NotRegistered':
      raise DeleteSessionException()
    raise PushNotificationException(http_response.text)


class NullDevicePushServiceProvider(DevicePushServiceProviderInterface):

  def Push(self, device, message):
    pass


class MockDevicePushServiceProvider(DevicePushServiceProviderInterface):

  def __init__(self):
    self.notifications = []

  def Push(self, device_token, title, message):
    if UPDATE_THROW_ERROR in message:
      self.notifications.append(Notification(device_token, title, message))
      raise UpdateDeviceTokenException(message[len(UPDATE_THROW_ERROR):])
    elif DELETE_THROW_ERROR in message:
      raise DeleteSessionException()
    elif PUSH_THROW_ERROR in message:
      raise PushNotificationException()
    self.notifications.append(Notification(device_token, title, message))


@singleton_util.Singleton()
class DevicePusher(object):
  
  def __init__(self):
    self.device_push_service_provider_dict = {}

  def AddDevicePushServiceProvider(self, device_type, device_push_service_provider):
    self.device_push_service_provider_dict[device_type] = device_push_service_provider

  def HasDevicePushServiceProvider(self, device_type):
    return device_type in self.device_push_service_provider_dict

  def Push(self, device_type, device_token, title, message):
    device_push_service_provider = self.device_push_service_provider_dict[device_type]
    device_push_service_provider.Push(device_token, title, message)
