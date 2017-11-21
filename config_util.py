import os
import ConfigParser


def GetConfig(filename):
  config = ConfigParser.ConfigParser()
  config.read(os.environ[filename])
  return config
