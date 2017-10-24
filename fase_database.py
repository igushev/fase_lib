import singleton_util


@singleton_util.Singleton()
class FaseDatabaseInterface(object):

  def AddService(self, service, overwrite=False):
    raise NotImplemented()

  def GetService(self, session_id):
    raise NotImplemented()

  def AddScreen(self, screen, overwrite=False):
    raise NotImplemented()

  def GetScreen(self, session_id):
    raise NotImplemented()


class MockFaseDatabase(FaseDatabaseInterface):

  def __init__(self, service_list, screen_list):
    self.session_id_to_service = {
        service._session_id: service for service in service_list}
    self.session_id_to_screen = {
        screen._session_id: screen for screen in screen_list}

  def AddService(self, service, overwrite=False):
    assert service._session_id not in self.session_id_to_service or overwrite
    self.session_id_to_service[service._session_id] = service

  def GetService(self, session_id):
    return self.session_id_to_service[session_id]

  def AddScreen(self, screen, overwrite=False):
    assert screen._session_id not in self.session_id_to_screen or overwrite
    self.session_id_to_screen[screen._session_id] = screen

  def GetScreen(self, session_id):
    return self.session_id_to_screen[session_id]
  