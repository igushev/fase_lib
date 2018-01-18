import fase_database
import fase_model
import fase
import singleton_util


STATUS_OK_TEXT = 'OK'

CREATE_DB_COMMAND = 'createdb'
DELETE_DB_COMMAND = 'deletedb'

TABLES_CREATED = 'Add table are being created'
TABLES_DELETED = 'All tables are being deleted'

DATETIME_FORMAT_HASH = '%Y%m%d%H%M%S%f'

WRONG_COMMAND = fase_model.BadRequest(
  code=401,
  message='Wrong command!')


class BadRequestException(Exception):

  def __init__(self, bad_request):
    super(BadRequestException, self).__init__()
    self._bad_request = bad_request

  def BadRequest(self):
    return self._bad_request


@singleton_util.Singleton()
class FaseServer(object):

  def SendInternalCommand(self, command):
    if command.command == CREATE_DB_COMMAND:
      fase_database.FaseDatabaseInterface.Get().CreateDatabase()
      return fase_model.Status(TABLES_CREATED)
    elif command.command == DELETE_DB_COMMAND:
      fase_database.FaseDatabaseInterface.Get().DeleteDatabase()
      return fase_model.Status(TABLES_DELETED)
    else:
      raise BadRequestException(WRONG_COMMAND)

  def SendServiceCommand(self, command):
    assert fase.Service.service_cls is not None
    service_cls = fase.Service.service_cls
    return fase_model.Status(service_cls.ServiceCommand(command))

  def GetService(self, device):
    assert fase.Service.service_cls is not None
    service_cls = fase.Service.service_cls

    service = service_cls()
    screen_prog = fase_model.ScreenProg(session_id=service.GetSessionId(), screen=service.OnStart())
    fase_database.FaseDatabaseInterface.Get().AddService(service)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog)

    return fase_model.Response(screen=screen_prog.screen,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  def GetScreen(self, session_info):
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    return fase_model.Response(screen=screen_prog.screen,
                               session_info=session_info,
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  @staticmethod
  def _GetElement(screen, id_list):
    element = screen
    for id_ in id_list:
      element = element.GetElement(id_)
    return element

  @staticmethod
  def _ScreenUpdate(screen, screen_update):
    for id_list, value in zip(screen_update.id_list_list, screen_update.value_list):
      FaseServer._GetElement(screen, id_list).Update(value)

  @staticmethod
  def ScreenUpdateToDict(screen_update):
    return {tuple(id_list): value for id_list, value in zip(screen_update.id_list_list, screen_update.value_list)}

  @staticmethod
  def _DictToScreenUpdate(id_list_to_value):
    id_list_list = []
    value_list = []
    for id_list_update, value in id_list_to_value.items():
      id_list_list.append(list(id_list_update))
      value_list.append(value)
    return fase_model.ScreenUpdate(id_list_list=id_list_list, value_list=value_list)

  @staticmethod
  def _UpdateScreenUpdate(current_screen_update, screen_update):
    current_id_list_to_value = (
        FaseServer.ScreenUpdateToDict(current_screen_update) if current_screen_update is not None else {})
    id_list_to_value = FaseServer.ScreenUpdateToDict(screen_update)
    current_id_list_to_value.update(id_list_to_value)
    return FaseServer._DictToScreenUpdate(current_id_list_to_value)

  def ScreenUpdate(self, screen_update, session_info, screen_info):
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If given screen_id is no longer relevant, just send current screen
    if screen_prog.screen.GetScreenId() != screen_info.screen_id:
      return fase_model.Response(screen=screen_prog.screen,
                                 session_info=fase_model.SessionInfo(service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

    FaseServer._ScreenUpdate(screen_prog.screen, screen_update)
    screen_prog.screen_update = FaseServer._UpdateScreenUpdate(screen_prog.screen_update, screen_update)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    return fase_model.Response(screen=screen_prog.screen,
                               screen_update=screen_prog.screen_update,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=screen_info)

  def ElementClicked(self, element_clicked, session_info, screen_info):
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If given screen_id is no longer relevant, just send current screen
    if screen_prog.screen.GetScreenId() != screen_info.screen_id:
      return fase_model.Response(screen=screen_prog.screen,
                                 session_info=fase_model.SessionInfo(service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

    if element_clicked.screen_update is not None:
      FaseServer._ScreenUpdate(screen_prog.screen, element_clicked.screen_update)
    element = FaseServer._GetElement(screen_prog.screen, element_clicked.id_list)
    service, screen = element.FaseOnClick(service, screen_prog.screen)
    screen_prog = fase_model.ScreenProg(session_id=service.GetSessionId(), screen=screen)
    fase_database.FaseDatabaseInterface.Get().AddService(service, overwrite=True)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    return fase_model.Response(screen=screen_prog.screen,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))
