import os
import sys


import fase


def GetResourceDir():
  return os.path.dirname(sys.modules[fase.Service.service_cls.__module__].__file__)
  