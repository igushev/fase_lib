import singleton_util


@singleton_util.Singleton()
class FaseDatabaseInterface(object):

  def AddService(self, service):
    raise NotImplemented()

  def GetService(self, session_id):
    raise NotImplemented()

  def AddScreen(self, screen):
    raise NotImplemented()

  def GetScreen(self, session_id):
    raise NotImplemented()
