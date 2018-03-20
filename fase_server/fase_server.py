import copy

from base_util import singleton_util

from fase import fase
from fase_model import fase_model

try:
  from . import fase_database
except SystemError:
  import fase_database


STATUS_OK_TEXT = 'OK'

CREATE_DB_COMMAND = 'createdb'
DELETE_DB_COMMAND = 'deletedb'

TABLES_CREATED = 'Add table are being created'
TABLES_DELETED = 'All tables are being deleted'

DATETIME_FORMAT = '%Y%m%d%H%M%S%f'

WRONG_COMMAND = fase_model.BadRequest(
  code=401,
  message='Wrong command!')


class BadRequestException(Exception):

  def __init__(self, bad_request):
    super(BadRequestException, self).__init__()
    self._bad_request = bad_request

  def BadRequest(self):
    return self._bad_request


def _PrepareScreen(obj, resource_set):
  assert isinstance(obj, fase.Element)
  if isinstance(obj, fase.Image) and obj.GetFilename():
    resource_set.add(fase_model.Resource(filename=obj.GetFilename()))
  if not isinstance(obj, fase.ElementContainer):
    return obj
  obj = copy.copy(obj)
  obj.id_element_list = [
      (id_, _PrepareScreen(element, resource_set))
      for id_, element in obj.id_element_list
      if not isinstance(element, fase.Variable)]
  return obj


def PrepareScreen(obj):
  resource_set = set()
  screen = _PrepareScreen(obj, resource_set)
  resources = fase_model.Resources(resource_list=list(resource_set)) if resource_set else None
  return screen, resources


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
    service._device_list.append(device)
    screen_prog = fase_model.ScreenProg(
        session_id=service.GetSessionId(), screen=service.OnStart(), recent_device=device)
    fase_database.FaseDatabaseInterface.Get().AddService(service)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog)

    screen, resources = PrepareScreen(screen_prog.screen)
    return fase_model.Response(screen=screen,
                               resources=resources,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  def GetScreen(self, device, session_info):
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)
    screen_prog.recent_device = device
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)
    screen, resources = PrepareScreen(screen_prog.screen)
    return fase_model.Response(screen=screen,
                               resources=resources,
                               session_info=session_info,
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  @staticmethod
  def _UpdateScreen(screen, elements_update):
    for id_list, value in zip(elements_update.id_list_list, elements_update.value_list):
      fase_model.GetScreenElement(screen, id_list).Update(value)

  @staticmethod
  def _UpdateElementsUpdate(current_elements_update, elements_update):
    current_id_list_to_value = (
        fase_model.ElementsUpdateToDict(current_elements_update) if current_elements_update is not None else {})
    id_list_to_value = fase_model.ElementsUpdateToDict(elements_update)
    current_id_list_to_value.update(id_list_to_value)
    return fase_model.DictToElementsUpdate(current_id_list_to_value) if current_id_list_to_value else None

  def ScreenUpdate(self, screen_update, session_info, screen_info):
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If given screen_id is no longer relevant, just send current screen
    if screen_prog.screen.GetScreenId() != screen_info.screen_id:
      screen, resources = PrepareScreen(screen_prog.screen)
      return fase_model.Response(screen=screen,
                                 resources=resources,
                                 session_info=fase_model.SessionInfo(service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

    same_device = screen_prog.recent_device == screen_update.device 

    if screen_update.elements_update is not None: 
      FaseServer._UpdateScreen(screen_prog.screen, screen_update.elements_update)
      screen_prog.elements_update = (
          FaseServer._UpdateElementsUpdate(screen_prog.elements_update, screen_update.elements_update))
      screen_prog.recent_device = screen_update.device
      fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    elements_update = screen_prog.elements_update if not same_device else None

    return fase_model.Response(elements_update=elements_update,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=screen_info)

  def _GetElement(self, screen, element_callback):
    element = fase_model.GetScreenElement(screen, element_callback.id_list)
    element.SetLocale(element_callback.locale)
    return element

  def ElementCallback(self, element_callback, session_info, screen_info):
    service = fase_database.FaseDatabaseInterface.Get().GetService(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If given screen_id is no longer relevant, just send current screen
    if screen_prog.screen.GetScreenId() != screen_info.screen_id:
      screen, resources = PrepareScreen(screen_prog.screen)
      return fase_model.Response(screen=screen,
                                 resources=resources,
                                 session_info=fase_model.SessionInfo(service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

    if element_callback.elements_update is not None:
      FaseServer._UpdateScreen(screen_prog.screen, element_callback.elements_update)
    element = self._GetElement(screen_prog.screen, element_callback)
    service, screen = (
        element.CallCallback(service, screen_prog.screen, element_callback.device, element_callback.method))
    screen.UpdateScreenId(service)
    screen_prog = fase_model.ScreenProg(
        session_id=service.GetSessionId(), screen=screen, recent_device=element_callback.device)
    fase_database.FaseDatabaseInterface.Get().AddService(service, overwrite=True)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    screen, resources = PrepareScreen(screen_prog.screen)
    return fase_model.Response(screen=screen,
                               resources=resources,
                               session_info=fase_model.SessionInfo(service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))
