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
  for device in service._device_list:
    if device_pusher.DevicePusher.Get().HasDevicePushServiceProvider(device.device_type):
      device_pusher.DevicePusher.Get().Push(device.device_type, device.device_token, title, message)
