from server_util import activation_code_generator
from server_util import config_util
from server_util import device_pusher
from server_util import sms_sender

try:
  from . import fase_database
  from . import fase_server
except SystemError:
  import fase_database
  import fase_server


def GetFaseDatabase(config):
  return fase_database.DynamoDBFaseDatabase(
      tables_suffix=config.get('database', 'tables_suffix'),
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


def GetDevicePusher(config):
  device_pusher_ = device_pusher.DevicePusher()
  if config.has_section('ios'):
    ios_device_push_service_provider = device_pusher.iOSDevicePushServiceProvider(
        server_url=config.get('ios', 'server_url'),
        key_id=config.get('ios', 'key_id'),
        team_id=config.get('ios', 'team_id'),
        key_file=config.get('ios', 'key_file'),
        app_id=config.get('ios', 'app_id'))
    device_pusher_.AddDevicePushServiceProvider(device_pusher.IOS, ios_device_push_service_provider)
  if config.has_section('android'):
    android_device_push_service_provider = device_pusher.AndroidDevicePushServiceProvider(
        server_url=config.get('android', 'server_url'),
        app_id=config.get('android', 'app_id'))
    device_pusher_.AddDevicePushServiceProvider(device_pusher.ANDROID, android_device_push_service_provider)
  return device_pusher_


fase_config = config_util.GetConfig('FASE_CONFIG_FILENAME')
fase_database.FaseDatabaseInterface.Set(GetFaseDatabase(fase_config))
activation_code_generator.ActivationCodeGenerator.Set(activation_code_generator.ActivationCodeGenerator())
sms_sender.SMSSender.Set(GetSMSSender(fase_config))
device_pusher.DevicePusher.Set(GetDevicePusher(config))
fase_server.FaseServer.Set(fase_server.FaseServer())
