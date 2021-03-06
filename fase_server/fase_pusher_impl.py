import logging
import sys

from fase_lib import fase_pusher
from fase_lib.server_util import device_pusher 

try:
  from fase_lib.fase_server import fase_database
  from fase_lib.fase_server import fase_sign_in_impl
except ImportError:
  import fase_database
  import fase_sign_in_impl


# Register itself as API implementation.
fase_pusher.fase_pusher_impl = sys.modules[__name__]


def Push(user_id, title, message):
  session_id = fase_sign_in_impl.GenerateSignedInSessionId(user_id)
  service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id)
  if service_prog is None:
    return
  device_list = []
  for device in service_prog.device_list:
    if device_pusher.DevicePusher.Get().HasDevicePushServiceProvider(device.device_type):
      if device.device_token:
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
  service_prog.device_list = device_list 
  fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog, overwrite=True)
