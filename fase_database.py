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

  def __init__(self, service_list, screen_list, user_list):
    self.session_id_to_service = {
        service._session_id: service for service in service_list}
    self.session_id_to_screen = {
        screen._session_id: screen for screen in screen_list}
    self.user_id_to_user = {
        user.user_id: user for user in user_list}

  def AddService(self, service, overwrite=False):
    assert service._session_id not in self.session_id_to_service or overwrite
    self.session_id_to_service[service._session_id] = service

  def HasService(self, session_id):
    return session_id in self.session_id_to_service

  def GetService(self, session_id):
    return self.session_id_to_service[session_id]

  def DeleteService(self, session_id):
    del self.session_id_to_service[session_id]

  def AddScreen(self, screen, overwrite=False):
    assert screen._session_id not in self.session_id_to_screen or overwrite
    self.session_id_to_screen[screen._session_id] = screen

  def HasScreen(self, session_id):
    return session_id in self.session_id_to_screen

  def GetScreen(self, session_id):
    return self.session_id_to_screen[session_id]

  def DeleteScreen(self, session_id):
    del self.session_id_to_screen[session_id]

  def AddUser(self, user, overwrite=False):
    assert user.user_id not in self.user_id_to_user or overwrite
    self.user_id_to_user[user.user_id] = user

  def GetUser(self, user_id):
    return self.user_id_to_user[user_id]

  def GetUserByPhoneNumber(self, phone_number):
    phone_number_user = [
        user for user in self.user_id_to_user.itervalues()
        if user.phone_number == phone_number]
    assert len(phone_number_user) == 1
    return phone_number_user[0]

  def GetSessionIdToService(self):
    return self.session_id_to_service
  
  def GetSessionIdToScreen(self):
    return self.session_id_to_screen
  
  def GetUserIdToUser(self):
    return self.user_id_to_user
