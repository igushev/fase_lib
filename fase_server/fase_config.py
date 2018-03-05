from server_util import activation_code_generator
from server_util import config_util
from server_util import sms_sender

try:
  from . import fase_database
  from . import fase_server
except SystemError:
  import fase_database
  import fase_server



def GetFaseDatabase(config):
  return fase_database.DynamoDBFaseDatabase(
      region_name=config.get('dynamodb', 'region_name'))


def GetSMSSender(config):
  if config.has_section('sns'):
    sms_service_provider = sms_sender.SNSSMSServiceProvider(
        region_name=config.get('sns', 'region_name'))
  else:
    sms_service_provider = sms_sender.NullSMSServiceProvider()
  return sms_sender.SMSSender(
      sms_service_provider=sms_service_provider,
      intercept_to=(
          config.get('sms_sender', 'intercept_to')
          if config.has_option('sms_sender', 'intercept_to')
          else None))


fase_config = config_util.GetConfig('FASE_CONFIG_FILENAME')
fase_database.FaseDatabaseInterface.Set(GetFaseDatabase(fase_config))
activation_code_generator.ActivationCodeGenerator.Set(activation_code_generator.ActivationCodeGenerator())
sms_sender.SMSSender.Set(GetSMSSender(fase_config))
fase_server.FaseServer.Set(fase_server.FaseServer())
