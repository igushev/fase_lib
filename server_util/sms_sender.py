import boto3
from collections import namedtuple

from fase_lib.base_util import singleton_util


THROW_ERROR = 'Include text to throw error'
SMS = namedtuple('SMS', ['phone_number', 'message'])


class SMSServiceProviderInterface(object):

  def Send(self, phone_number, message):
    raise NotImplemented()


class SNSSMSServiceProvider(SMSServiceProviderInterface):
  
  def __init__(self, **kw_params):
    self._sns_client = boto3.client('sns', **kw_params)
    self._sns_client.set_sms_attributes(
        attributes={
            'DefaultSMSType': 'Transactional'})

  def Send(self, phone_number, message):
    self._sns_client.publish(PhoneNumber=phone_number, Message=message)


class NullSMSServiceProvider(SMSServiceProviderInterface):

  def Send(self, phone_number, message):
    pass


class PrintSMSServiceProvider(SMSServiceProviderInterface):

  def Send(self, phone_number, message):
    print('Sending %s to %s' % (message, phone_number))


class MockSMSServiceProviderException(Exception):
  pass


class MockSMSServiceProvider(SMSServiceProviderInterface):

  def __init__(self):
    self.smss = []

  def Send(self, phone_number, message):
    if THROW_ERROR in message:
      raise MockSMSServiceProviderException()
    self.smss.append(SMS(phone_number, message))


@singleton_util.Singleton()
class SMSSender(object):
  
  def __init__(self, sms_service_provider, intercept_to=None):
    self.sms_service_provider = sms_service_provider
    self.intercept_to = intercept_to

  def Send(self, phone_number, message):
    self.sms_service_provider.Send(self.intercept_to or phone_number, message)
