import os
import configparser


def GetConfigByFilename(filename):
  config = configparser.ConfigParser()
  config.read(filename)
  return config


def GetConfig(env_var_name):
  return GetConfigByFilename(os.environ[env_var_name])
