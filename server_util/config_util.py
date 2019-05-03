import os
import configparser


def GetConfigFromFile(filename):
  config = configparser.ConfigParser()
  config.read(filename)
  return config
