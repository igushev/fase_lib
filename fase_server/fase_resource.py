import os
import sys


from fase_lib import fase


def GetResourceDir():
  return os.path.dirname(sys.modules[fase.Service.service_cls.__module__].__file__)
  