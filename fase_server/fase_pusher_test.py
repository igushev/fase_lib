import datetime
import unittest

from server_util import device_pusher 

from fase import fase_pusher
from fase import fase
from fase_model import fase_model

import fase_database
import fase_pusher_impl
import fase_sign_in_impl


class PusherTestService(fase.Service):

  service_id = 'PusherTest'

  @staticmethod
  def GetServiceId():
    return PusherTestService.service_id

  def OnStart(self):
    return fase.Screen(self)


fase.Service.RegisterService(PusherTestService)


class FasePusherTest(unittest.TestCase):

  def AssertNotification(self, device_token, notification):
    self.assertEqual(device_token, notification.device_token)
    self.assertEqual('TestTitle', notification.title)
    self.assertEqual('TestMessage', notification.message)

  def AddDevicePushServiceProviderAndService(self):
    device_pusher.DevicePusher.Set(device_pusher.DevicePusher(), overwrite=True)
    device_type_1_provider = device_pusher.MockDevicePushServiceProvider()
    device_pusher.DevicePusher.Get().AddDevicePushServiceProvider('device_type_1', device_type_1_provider)
    device_type_2_provider = device_pusher.MockDevicePushServiceProvider()
    device_pusher.DevicePusher.Get().AddDevicePushServiceProvider('device_type_2', device_type_2_provider)
    
    user = fase.User(user_id='321',
                     phone_number='+13216549870',
                     first_name='Edward',
                     last_name='Igushev',
                     datetime_added=datetime.datetime.utcnow())
    service = PusherTestService()
    service._session_id = fase_sign_in_impl.GenerateSignedInSessionId(user.user_id)
    service._device_list.append(fase.Device(device_type='device_type_1', device_token='device_token_1_1'))
    service._device_list.append(fase.Device(device_type='device_type_1', device_token='device_token_1_2'))
    service._device_list.append(fase.Device(device_type='device_type_2', device_token='device_token_2_1'))
    screen = service.OnStart()
    service_prog = fase_model.ServiceProg(session_id=service.GetSessionId(), service=service)
    screen_prog = fase_model.ScreenProg(session_id=service.GetSessionId(), screen=screen)

    fase_database.FaseDatabaseInterface.Set(
        fase_database.MockFaseDatabase(
            service_prog_list=[service_prog],
            screen_prog_list=[screen_prog],
            user_list=[user]),
        overwrite=True)
    return device_type_1_provider, device_type_2_provider, service, user

  def testGeneral(self):
    device_type_1_provider, device_type_2_provider, _, user = (
        self.AddDevicePushServiceProviderAndService())

    fase_pusher.Push(user.user_id, 'TestTitle', 'TestMessage')
    
    self.assertEqual(2, len(device_type_1_provider.notifications))
    self.AssertNotification('device_token_1_1', device_type_1_provider.notifications[0])
    self.AssertNotification('device_token_1_2', device_type_1_provider.notifications[1])
    self.assertEqual(1, len(device_type_2_provider.notifications))
    self.AssertNotification('device_token_2_1', device_type_2_provider.notifications[0])

  def testUpdate(self):
    device_type_1_provider, device_type_2_provider, service, user = (
        self.AddDevicePushServiceProviderAndService())

    fase_pusher.Push(user.user_id, 'TestTitle', device_pusher.UPDATE_THROW_ERROR + 'device_token_1b')
    
    self.assertEqual(2, len(device_type_1_provider.notifications))
    self.assertEqual(1, len(device_type_2_provider.notifications))

    self.assertEqual(3, len(service._device_list))
    self.assertEqual(fase.Device(device_type='device_type_1', device_token='device_token_1b'), service._device_list[0])
    self.assertEqual(fase.Device(device_type='device_type_1', device_token='device_token_1b'), service._device_list[1])
    self.assertEqual(fase.Device(device_type='device_type_2', device_token='device_token_1b'), service._device_list[2])

  def testDelete(self):
    device_type_1_provider, device_type_2_provider, service, user = (
        self.AddDevicePushServiceProviderAndService())

    fase_pusher.Push(user.user_id, 'TestTitle', device_pusher.DELETE_THROW_ERROR)
    
    self.assertEqual(0, len(device_type_1_provider.notifications))
    self.assertEqual(0, len(device_type_2_provider.notifications))
    self.assertEqual(0, len(service._device_list))
    

if __name__ == '__main__':
    unittest.main()
