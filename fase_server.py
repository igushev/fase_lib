import logging
import traceback

import fase_error
import fase


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500


class BadRequestException(Exception):

  def __init__(self, bad_request):
    super(BadRequestException, self).__init__()
    self._bad_request = bad_request

  def BadRequest(self):
    return self._bad_request


class FaseServer(object):

  @staticmethod
  def _SafeCall(func, *args, **kwargs):
    try:
      res = func(*args, **kwargs)
      return res, STATUS_OK
    except BadRequestException as bad_request_exception:
      return bad_request_exception.BadRequest(), STATUS_BAD_REQUEST
    except Exception as e:
      logging.error(type(e))
      logging.error(str(e))
      logging.error(str(traceback.format_exc()))
      return str(traceback.format_exc()), STATUS_ERROR


  def GetService(self, service_name, device):
    # Check in database, maybe return existing screen
    if service_name not in fase.service_dict:
      raise BadRequestException(fase_error.SERVICE_NOT_FOUND)
    service_cls = fase.service_dict[service_name]
    service_obj = service_cls()
    screen = service_obj.OnStart()
    # Save screen into database
    return screen

  def GetScreen(self):
    # Get current screen.
    pass

  def ScreenUpdate(self):
    # Update screen in database
    pass

  def ScreenClicked(self):
    # Call feedback, update database and return new screen.
    pass
