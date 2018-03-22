import logging
import sys

from server_util import device_pusher 

from fase import fase_pusher

try:
  from . import fase_database
  from . import fase_sign_in_impl
except SystemError:
  import fase_database
  import fase_sign_in_impl


# Register itself as API implementation.
fase_pusher.fase_pusher_impl = sys.modules[__name__]


def Push(user_id, title, message):
  session_id = fase_sign_in_impl.GenerateSignedInSessionId(user_id)
  service = fase_database.FaseDatabaseInterface.Get().GetService(session_id)
  device_list = []
  for device in service._device_list:
    if device_pusher.DevicePusher.Get().HasDevicePushServiceProvider(device.device_type):
      try:
        device_pusher.DevicePusher.Get().Push(device.device_type, device.device_token, title, message)
      except device_pusher.UpdateDeviceTokenException as e:
        device.device_token = e.device_token
      except device_pusher.DeleteSessionException:
        continue
      except Exception as e:
        logging.error('Error pushing notification')
        logging.error(type(e))
        logging.error(str(e))
      device_list.append(device)
  service._device_list = device_list 
  service = fase_database.FaseDatabaseInterface.Get().AddService(service, overwrite=True)
