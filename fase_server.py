import datetime
import hashlib
import logging
import traceback

import fase_database
import fase_error
import fase_model
import fase
import singleton_util


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500
STATUS_OK_TEXT = 'OK'

CREATE_DB_COMMAND = 'createdb'
DELETE_DB_COMMAND = 'deletedb'

TABLE_CREATED = 'Table %s created'
TABLE_EXISTED = 'Table %s already existed'
TABLES_DELETED = 'All tables are being deleted'

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'

DELETING_DB_IS_NOT_ALLOWED = fase_model.BadRequest(
  code=401,
  message='Deleting of database is not allowed by the configuration!')
WRONG_COMMAND = fase_model.BadRequest(
  code=402,
  message='Wrong command!')


class BadRequestException(Exception):

  def __init__(self, bad_request):
    super(BadRequestException, self).__init__()
    self._bad_request = bad_request

  def BadRequest(self):
    return self._bad_request


@singleton_util.Singleton()
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

  def SendCommand(self, command):
    if command.command == CREATE_DB_COMMAND:
      table_statuses_dict = self.database.CreateDB()
      table_statuses_str = [
          TABLE_CREATED % table_name
          if table_status.created
          else TABLE_EXISTED % table_name
          for table_name, table_status
          in table_statuses_dict.iteritems()]
      return fase_model.Status('\n'.join(sorted(table_statuses_str)))
    elif command.command == DELETE_DB_COMMAND:
      if not self.processor_config.allow_deletedb:
        raise BadRequestException(DELETING_DB_IS_NOT_ALLOWED)
      self.database.DeleteDB()
      return fase_model.Status(TABLES_DELETED)
    else:
      raise BadRequestException(WRONG_COMMAND)

  def GetService(self, device):
    assert fase.Service.service_cls is not None
    service_cls = fase.Service.service_cls

    service = service_cls()
    screen = service.OnStart()
    fase_database.FaseDatabaseInterface.Get().AddService(service)
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen)

    return fase_model.Response(screen=screen,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen.GetScreenId()))

  def GetScreen(self, session_info):
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))
    return fase_model.Response(screen=screen,
                               session_info=session_info,
                               screen_info=fase_model.ScreenInfo(screen.GetScreenId()))

  def _GetElement(self, screen, id_list):
    element = screen
    for id_ in id_list:
      element = element.GetElement(id_)
    return element

  def ScreenUpdate(self, screen_update, session_info, screen_info):
    service = (fase_database.FaseDatabaseInterface.Get().
               GetService(session_info.session_id))
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))

    # If given screen_id is no longer relevant, just send current screen
    if screen.GetScreenId() != screen_info.screen_id:
      return fase_model.Response(screen=screen,
                                 session_info=fase_model.SessionInfo(service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen.GetScreenId()))

    for id_list, value in zip(
        screen_update.id_list_list, screen_update.value_list):
      self._GetElement(screen, id_list).Update(value)
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)

    return fase_model.Response(screen=screen,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=screen_info)

  def ElementClicked(self, element_clicked, session_info, screen_info):
    service = (fase_database.FaseDatabaseInterface.Get().
               GetService(session_info.session_id))
    screen = (fase_database.FaseDatabaseInterface.Get().
              GetScreen(session_info.session_id))

    # If given screen_id is no longer relevant, just send current screen
    if screen.GetScreenId() != screen_info.screen_id:
      return fase_model.Response(screen=screen,
                                 session_info=fase_model.SessionInfo(service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen.GetScreenId()))

    element = self._GetElement(screen, element_clicked.id_list)
    service, screen = element.FaseOnClick(service, screen)
    fase_database.FaseDatabaseInterface.Get().AddService(service, overwrite=True)
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen, overwrite=True)

    return fase_model.Response(screen=screen,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen.GetScreenId()))

  ##############################################################################
  # Safe Methods

  def SendCommandSafe(self, command):
    return FaseServer._SafeCall(self.SendCommand, command)

  def GetServiceSafe(self, device):
    return FaseServer._SafeCall(self.GetService, device)

  def GetScreenSafe(self, session_info):
    return FaseServer._SafeCall(self.GetScreen, session_info)

  def ScreenUpdateSafe(self, screen_update, session_info, screen_info):
    return FaseServer._SafeCall(self.ScreenUpdate, screen_update, session_info, screen_info)

  def ElementClickedSafe(self, element_clicked, session_info, screen_info):
    return FaseServer._SafeCall(self.ElementClicked, element_clicked, session_info, screen_info)
