import activation_code_generator
import config_util
import fase_database
import fase_server
import sms_sender


def GetFaseDatabase(config):
  return fase_database.DynamoDBFaseDatabase(
      region_name=config.get('dynamodb', 'region_name'),
      endpoint_url=config.get('dynamodb', 'endpoint_url'),
      aws_access_key_id=config.get('dynamodb', 'aws_access_key_id'),
      aws_secret_access_key=config.get('dynamodb', 'aws_secret_access_key'))


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
      intercept_to=(
          config.get('sms_sender', 'intercept_to')
          if config.has_option('sms_sender', 'intercept_to')
          else None))


fase_config = config_util.GetConfig('FASE_CONFIG_FILENAME')
fase_database.FaseDatabase.Set(GetFaseDatabase(fase_config))
activation_code_generator.ActivationCodeGenerator.Set(GetActivationCodeGenerator(fase_config))
sms_sender.SMSSender.Set(GetSMSSender(fase_config))
fase_server.FaseServer.Set(fase_server.FaseServer())
