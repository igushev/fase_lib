import copy

from fase_lib import fase
from fase_lib.base_util import singleton_util
from fase_lib.server_util import device_pusher
from fase_lib.server_util import resource_manager
from fase_lib.fase_model import fase_model

try:
  from fase_lib.fase_server import fase_database
except ImportError:
  import fase_database


STATUS_OK_TEXT = 'OK'

CREATE_DB_COMMAND = 'createdb'
DELETE_DB_COMMAND = 'deletedb'

TABLES_CREATED = 'Add table are being created'
TABLES_DELETED = 'All tables are being deleted'

WRONG_COMMAND = fase_model.BadRequest(
  code=401,
  message='Wrong command!')
DELETING_DB_IS_NOT_ALLOWED = fase_model.BadRequest(
  code=402,
  message='Deleting of database is not allowed by the configuration!')


class BadRequestException(Exception):

  def __init__(self, bad_request):
    super(BadRequestException, self).__init__()
    self._bad_request = bad_request

  def BadRequest(self):
    return self._bad_request


def _PrepareScreen(obj, device, resource_set):
  assert isinstance(obj, fase.Element)
  if isinstance(obj, fase.Image) and obj.GetFilename():
    pixel_density = (device.pixel_density or 1.0) if device.device_type != device_pusher.IOS else 1.0
    pixel_density_mult = obj.GetPixelDensityMult() or 1.0
    filename = resource_manager.ResourceManager.Get().GetResourceFilename(
        obj.GetFilename(), pixel_density * pixel_density_mult)
    if filename is not None:
      resource_set.add(fase_model.Resource(filename=filename))
      obj = copy.copy(obj)
      obj.SetFilename(filename)
      return obj
    else:
      return None
  if not isinstance(obj, fase.ElementContainer):
    return obj
  obj = copy.copy(obj)
  obj.id_element_list = [
      (id_, _PrepareScreen(element, device, resource_set))
      for id_, element in obj.id_element_list
      if not isinstance(element, fase.Variable)]
  return obj


def PrepareScreen(obj, device):
  resource_set = set()
  screen = _PrepareScreen(obj, device, resource_set)
  resources = fase_model.Resources(resource_list=list(resource_set))
  return screen, resources


@singleton_util.Singleton()
class FaseServer(object):

  def __init__(self,
               allow_deletedb=False):
    self.allow_deletedb = allow_deletedb

  def SendInternalCommand(self, command):
    if command.command == CREATE_DB_COMMAND:
      fase_database.FaseDatabaseInterface.Get().CreateDatabase()
      return fase_model.Status(TABLES_CREATED)
    elif command.command == DELETE_DB_COMMAND:
      if not self.allow_deletedb:
        raise BadRequestException(DELETING_DB_IS_NOT_ALLOWED)
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
    device.device_id = device.device_id or device.device_token  # For backwards compatibility. 
    service_cls = fase.Service.service_cls
    latest_version = service_cls.Version()

    service_prog, screen_prog = fase_model.GetServiceProgScreenProg(device)
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog)

    screen, resources = PrepareScreen(screen_prog.screen, device)
    return fase_model.Response(screen=screen,
                               resources=resources,
                               version_info=fase_model.VersionInfo(version=latest_version),
                               session_info=fase_model.SessionInfo(service_prog.service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  @staticmethod
  def _ServiceUpdate(service_prog, screen_prog, device):
    assert fase.Service.service_cls is not None
    service_cls = fase.Service.service_cls
    latest_version = service_cls.Version()

    service_updated = service_cls()
    service_updated._session_id = service_prog.service._session_id
    service_updated._if_signed_in = service_prog.service._if_signed_in
    service_updated._user_id = service_prog.service._user_id
    service_updated._user = service_prog.service._user
    service_prog.service = service_updated 
    service_prog.version = latest_version
    screen_prog.screen = service_prog.service.OnUpdate()
    FaseServer._RefreshServiceProg(service_prog, screen_prog, device)
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog, overwrite=True)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    screen, resources = PrepareScreen(screen_prog.screen, device)
    resources.reset_resources = True
    return fase_model.Response(screen=screen,
                               resources=resources,
                               version_info=fase_model.VersionInfo(version=latest_version),
                               session_info=fase_model.SessionInfo(service_prog.service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  @staticmethod
  def _ServiceProgScreenProgUpdateDevice(service_prog, screen_prog, device):
    for device_signed_in in service_prog.device_list:
      if fase_model.SameDevice(device_signed_in, device):
        device_signed_in.device_token = device.device_token
        device_signed_in.pixel_density = device.pixel_density
    screen_prog.recent_device = device

  def GetScreen(self, device, version_info, session_info):
    assert fase.Service.service_cls is not None
    device.device_id = device.device_id or device.device_token  # For backwards compatibility. 
    service_cls = fase.Service.service_cls
    latest_version = service_cls.Version()

    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If current version is no longer relevant, update the Service.
    if latest_version != service_prog.version:
      return FaseServer._ServiceUpdate(service_prog, screen_prog, device)

    FaseServer._ServiceProgScreenProgUpdateDevice(service_prog, screen_prog, device)
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog, overwrite=True)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)
    screen, resources = PrepareScreen(screen_prog.screen, device)
    resources.reset_resources = latest_version != version_info.version
    return fase_model.Response(screen=screen,
                               resources=resources,
                               version_info=fase_model.VersionInfo(version=latest_version),
                               session_info=session_info,
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

  @staticmethod
  def _RefreshServiceProg(service_prog, screen_prog, device):
    screen_prog.screen.UpdateScreenId(service_prog.service)
    screen_prog.elements_update = None
    FaseServer._ServiceProgScreenProgUpdateDevice(service_prog, screen_prog, device)

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

  def ScreenUpdate(self, screen_update, version_info, session_info, screen_info):
    assert fase.Service.service_cls is not None
    # For backwards compatibility.
    screen_update.device.device_id = screen_update.device.device_id or screen_update.device.device_token 
    service_cls = fase.Service.service_cls
    latest_version = service_cls.Version()

    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If current version is no longer relevant, update the Service.
    if latest_version != service_prog.version:
      return FaseServer._ServiceUpdate(service_prog, screen_prog, screen_update.device)

    # If given screen_id is no longer relevant, just send current screen
    if screen_prog.screen.GetScreenId() != screen_info.screen_id:
      screen, resources = PrepareScreen(screen_prog.screen, screen_update.device)
      resources.reset_resources = latest_version != version_info.version
      return fase_model.Response(screen=screen,
                                 resources=resources,
                                 version_info=fase_model.VersionInfo(version=latest_version),
                                 session_info=fase_model.SessionInfo(service_prog.service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

    same_device = fase_model.SameDevice(screen_prog.recent_device, screen_update.device) 

    if screen_update.elements_update is not None:
      FaseServer._UpdateScreen(screen_prog.screen, screen_update.elements_update)
      screen_prog.elements_update = (
          FaseServer._UpdateElementsUpdate(screen_prog.elements_update, screen_update.elements_update))
      FaseServer._ServiceProgScreenProgUpdateDevice(service_prog, screen_prog, screen_update.device)
      fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog, overwrite=True)
      fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    elements_update = screen_prog.elements_update if not same_device else None

    return fase_model.Response(elements_update=elements_update,
                               version_info=fase_model.VersionInfo(version=latest_version),
                               session_info=fase_model.SessionInfo(service_prog.service.GetSessionId()),
                               screen_info=screen_info)

  def _GetElement(self, screen, element_callback):
    element = fase_model.GetScreenElement(screen, element_callback.id_list)
    element.SetLocale(element_callback.locale)
    return element

  def ElementCallback(self, element_callback, version_info, session_info, screen_info):
    assert fase.Service.service_cls is not None
    # For backwards compatibility.
    element_callback.device.device_id = element_callback.device.device_id or element_callback.device.device_token 
    service_cls = fase.Service.service_cls
    latest_version = service_cls.Version()

    service_prog = fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_info.session_id)
    screen_prog = fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_info.session_id)

    # If current version is no longer relevant, update the Service.
    if latest_version != service_prog.version:
      return FaseServer._ServiceUpdate(service_prog, screen_prog, element_callback.device)

    # If given screen_id is no longer relevant, just send current screen
    if screen_prog.screen.GetScreenId() != screen_info.screen_id:
      screen, resources = PrepareScreen(screen_prog.screen, element_callback.device)
      resources.reset_resources = latest_version != version_info.version
      return fase_model.Response(screen=screen,
                                 resources=resources,
                                 version_info=fase_model.VersionInfo(version=latest_version),
                                 session_info=fase_model.SessionInfo(service_prog.service.GetSessionId()),
                                 screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))

    if element_callback.elements_update is not None:
      FaseServer._UpdateScreen(screen_prog.screen, element_callback.elements_update)
    element = self._GetElement(screen_prog.screen, element_callback)
    service_prog, screen_prog = element.CallCallback(
        service_prog, screen_prog, element_callback.device, element_callback.method)
    FaseServer._RefreshServiceProg(service_prog, screen_prog, element_callback.device)
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog, overwrite=True)
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog, overwrite=True)

    screen, resources = PrepareScreen(screen_prog.screen, element_callback.device)
    return fase_model.Response(screen=screen,
                               resources=resources,
                               version_info=fase_model.VersionInfo(version=latest_version),
                               session_info=fase_model.SessionInfo(service_prog.service.GetSessionId()),
                               screen_info=fase_model.ScreenInfo(screen_prog.screen.GetScreenId()))
