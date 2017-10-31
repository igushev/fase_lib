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

  def GetService(self, device):
    assert fase.Service.service_cls is not None
    service_cls = fase.Service.service_cls

    service = service_cls()
    service._sessino_id = fase.GenerateSessionId()
    service._datetime_added = datetime.datetime.now()
    screen = service.OnStart()
    fase_database.FaseDatabaseInterface.Get().AddService(service)
    screen._session_id = service._session_id
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen)

    return fase_model.Response(screen=screen,
                               session_info=fase_model.SessionInfo(service._session_id),
                               screen_info=fase_model.ScreenInfo(screen._screen_id))

  def GetScreen(self, session_info):
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))
    return fase_model.Response(screen=screen,
                               session_info=session_info,
                               screen_info=fase_model.ScreenInfo(screen._screen_id))

  def _GetElement(self, screen, id_list):
    element = screen
    for id_ in id_list:
      element = element.GetElement(id_)
    return element

  # TODO(igushev): Generate screen_id and compare with received one.
  # TODO(igushev): Return either OK or another screen.
  def ScreenUpdate(self, screen_update, session_info, screen_info):
    service = (fase_database.FaseDatabaseInterface.Get().
               GetService(session_info.session_id))
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))

    # If given screen_id is no longer relevant, just send current screen
    if screen._screen_id != screen_info.screen_id:
      return fase_model.Response(screen=screen,
                                 session_info=fase_model.SessionInfo(service._session_id),
                                 screen_info=fase_model.ScreenInfo(screen._screen_id))

    for id_list, value in zip(
        screen_update.id_list_list, screen_update.value_list):
      self._GetElement(screen, id_list).Update(value)
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)

    return fase_model.Response(screen=screen,
                               session_info=fase_model.SessionInfo(service._session_id),
                               screen_info=screen_info)

  def ElementClicked(self, element_clicked, session_info, screen_info):
    service = (fase_database.FaseDatabaseInterface.Get().
               GetService(session_info.session_id))
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))

    # If given screen_id is no longer relevant, just send current screen
    if screen._screen_id != screen_info.screen_id:
      return fase_model.Response(screen=screen,
                                 session_info=fase_model.SessionInfo(service._session_id),
                                 screen_info=fase_model.ScreenInfo(screen._screen_id))

    element = self._GetElement(screen, element_clicked.id_list)
    service, screen = element.FaseOnClick(service, screen)
    fase_database.FaseDatabaseInterface.Get().AddService(service, overwrite=True)
    screen._session_id = service._session_id
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)

    return fase_model.Response(screen=screen,
                               session_info=fase_model.SessionInfo(service._session_id),
                               screen_info=fase_model.ScreenInfo(screen._screen_id))

