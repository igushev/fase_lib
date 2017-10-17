import collections
import os
import ConfigParser

from boto.dynamodb2.layer1  import DynamoDBConnection

import activation_code_generator
import sms_sender
import fase_database


DatabaseConfig = collections.namedtuple('DatabaseConfig', ['tables_suffix'])


def GetConfig(filename):
  config = ConfigParser.ConfigParser()
  config.read(os.environ[filename])
  return config


def GetDynamoDBConnection(config):
  return DynamoDBConnection(
      region=config.get('dynamodb', 'region')
      if config.has_option('dynamodb', 'region') else None,
      host=config.get('dynamodb', 'host')
      if config.has_option('dynamodb', 'host') else None,
      port=config.getint('dynamodb', 'port')
      if config.has_option('dynamodb', 'port') else None,
      aws_access_key_id=config.get('dynamodb', 'aws_access_key_id')
      if config.has_option('dynamodb', 'aws_access_key_id') else None,
      aws_secret_access_key=config.get('dynamodb', 'aws_secret_access_key')
      if config.has_option('dynamodb', 'aws_secret_access_key') else None,
      is_secure=config.getboolean('dynamodb', 'is_secure')
      if config.has_option('dynamodb', 'is_secure') else None)


def GetDatabaseConfig(config):
  return DatabaseConfig(
      tables_suffix=config.get('database', 'tables_suffix')
      if config.has_option('database', 'tables_suffix') else None)


def GetActivationCodeGenerator(config):
  return activation_code_generator.ActivationCodeGenerator()


def GetSMSSender(config):
  if config.has_section('sns'):
    sms_service_provider = sms_sender.SNSSMSServiceProvider(
        region_name=config.get('sns', 'region_name'),
        aws_access_key_id=config.get('sns', 'aws_access_key_id'),
        aws_secret_access_key=config.get('sns', 'aws_secret_access_key'))
  else:
    sms_service_provider = sms_sender.NullSMSServiceProvider()
  return sms_sender.SMSSender(
      sms_service_provider=sms_service_provider,
      ios_link=config.get('sms_sender', 'ios_link'),
      andriod_link=config.get('sms_sender', 'andriod_link'),
      intercept_to=(
          config.get('sms_sender', 'intercept_to')
          if config.has_option('sms_sender', 'intercept_to')
          else None))



fase_config = GetConfig('FASE_CONFIG_FILENAME')
activation_code_generator.ActivationCodeGenerator.Set(GetActivationCodeGenerator(fase_config))
fase_database.FaseDatabase.Set(fase_database.FaseDatabase(
    GetDatabaseConfig(fase_config), GetDynamoDBConnection(fase_config)))
sms_sender.SMSSender.Set(GetSMSSender(fase_config))
