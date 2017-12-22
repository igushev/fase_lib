import os
import configparser


def GetConfig(filename):
  config = configparser.ConfigParser()
  config.read(os.environ[filename])
  return config
