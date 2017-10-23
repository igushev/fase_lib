import datetime
import hashlib
import logging
import traceback

import fase_database
import fase_error
import fase_model
import fase


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500
STATUS_OK_TEXT = 'OK'

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'


def CreateService(service_cls, device):
  service = service_cls()
  datetime_now = datetime.datetime.now()
  sessino_id_hash = hashlib.md5()
  sessino_id_hash.update(datetime_now.strftime(DATETIME_FORMAT_HASH))
  sessino_id_hash.update(device.device_type)
  sessino_id_hash.update(device.device_token)
  service._sessino_id = sessino_id_hash.hexdigest()
  service._datetime_added = datetime_now


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
    if service_name not in fase.service_dict:
      raise BadRequestException(fase_error.SERVICE_NOT_FOUND)
    service_cls = fase.service_dict[service_name]

    service = CreateService(service_cls)
    fase_database.FaseDatabaseInterface.Get().AddService(service)
    screen = service.OnStart()
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen)

    return fase_model.SessionInfo(screen._session_id)

  def GetScreen(self, session_info):
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))
    return screen

  def ScreenUpdate(self, screen_update, session_info):
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))
    for id_, value in screen_update.id_to_value.iteritems():
      screen.GetElement(id_).Update(value)
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)
    return fase_model.Status(STATUS_OK_TEXT)

  def ElementClicked(self, element_clicked, session_info):
    service = (fase_database.FaseDatabaseInterface.Get().
               GetService(session_info.session_id))
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))
    element = screen.GetElement(element_clicked.id_element)
    screen = element._on_click(service, screen)
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)
    return screen

