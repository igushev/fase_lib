import os
import sys


from fase import fase


def GetResourceDir():
  return os.path.dirname(sys.modules[fase.Service.service_cls.__module__].__file__)
  