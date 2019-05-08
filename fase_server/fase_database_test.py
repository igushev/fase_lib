import datetime
import os
import signal
import subprocess
import unittest

from fase_lib import fase
from fase_lib.fase_model import fase_model

from fase_lib.fase_server import fase_database


DYNAMODB_CMD = (
    'java'
    ' -Djava.library.path=~/DynamoDBLocal/DynamoDBLocal_lib'
    ' -jar ~/DynamoDBLocal/DynamoDBLocal.jar -inMemory')


class DatabaseTestService(fase.Service):

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddText(id_='text_name_id', hint='Enter Name')
    screen.AddButton(id_='next_button_id', text='Next', on_click=DatabaseTestService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetText(id_='text_name_id').GetText()
    screen = fase.Screen(self)
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id', text='Reset', on_click=DatabaseTestService.OnResetButton)
    return screen

  def OnResetButton(self, screen, element):
    # Ignore previous screen and element.
    return self.OnStart()


class DynamoDBFaseDatabaseTest(unittest.TestCase):

  def setUp(self):
    super(DynamoDBFaseDatabaseTest, self).setUp()
    self.dynamodb_process = (
        subprocess.Popen(DYNAMODB_CMD, shell=True, preexec_fn=os.setsid))
    fase_database.FaseDatabaseInterface.Set(
        fase_database.DynamoDBFaseDatabase(region_name='us-west-2',
                                           endpoint_url='http://localhost:8000',
                                           aws_access_key_id='Fase',
                                           aws_secret_access_key='Fase'),
        overwrite=True)

  def tearDown(self):
    os.killpg(self.dynamodb_process.pid, signal.SIGKILL)
    super(DynamoDBFaseDatabaseTest, self).tearDown()

  def testFase(self):
    fase_database.FaseDatabaseInterface.Get().CreateDatabase()

    service_1 = DatabaseTestService()
    screen_1 = service_1.OnStart()
    session_id_1 = service_1.GetSessionId()
    service_prog_1 = fase_model.ServiceProg(session_id=session_id_1, service=service_1)
    screen_prog_1 = fase_model.ScreenProg(session_id=session_id_1, screen=screen_1)

    service_2 = DatabaseTestService()
    screen_2 = service_2.OnStart()
    text_name = screen_2.GetElement(id_='text_name_id') 
    text_name.Update('Edward Igushev')
    screen_2 = service_2.OnNextButton(screen_2, text_name)
    session_id_2 = service_2.GetSessionId()
    service_prog_2 = fase_model.ServiceProg(session_id=session_id_2, service=service_2)
    screen_prog_2 = fase_model.ScreenProg(session_id=session_id_2, screen=screen_2)

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id_1))
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog_1)
    self.assertEqual(service_prog_1, fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id_1))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id_2))
    fase_database.FaseDatabaseInterface.Get().AddServiceProg(service_prog_2)
    self.assertEqual(service_prog_1, fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id_1))
    self.assertEqual(service_prog_2, fase_database.FaseDatabaseInterface.Get().GetServiceProg(session_id_2))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_id_1))
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog_1)
    self.assertEqual(screen_prog_1, fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_id_1))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_id_2))
    fase_database.FaseDatabaseInterface.Get().AddScreenProg(screen_prog_2)
    self.assertEqual(screen_prog_1, fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_id_1))
    self.assertEqual(screen_prog_2, fase_database.FaseDatabaseInterface.Get().GetScreenProg(session_id_2))
    
    datetime_now = datetime.datetime.utcnow().replace(microsecond=0)
    user_1 = fase.User(user_id='321',
                       phone_number='+13216549870',
                       first_name='Edward',
                       last_name='Igushev',
                       datetime_added=datetime_now)
    user_2 = fase.User(user_id='987',
                       phone_number='+19876543210',
                       first_name='Edward Junior',
                       last_name='Igushev',
                       datetime_added=datetime_now)
    user_2b = fase.User(user_id='987b',
                        phone_number='+19876543210',
                        first_name='Edward Junior',
                        last_name='Igushev (One more account)',
                        datetime_added=datetime_now)

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetUser(user_1.user_id))
    self.assertEqual([], fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_1.phone_number))
    fase_database.FaseDatabaseInterface.Get().AddUser(user_1)
    self.assertEqual(user_1, fase_database.FaseDatabaseInterface.Get().GetUser(user_1.user_id))
    self.assertEqual([user_1], fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_1.phone_number))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetUser(user_2.user_id))
    self.assertEqual([], fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_2.phone_number))
    fase_database.FaseDatabaseInterface.Get().AddUser(user_2)
    self.assertEqual(user_1, fase_database.FaseDatabaseInterface.Get().GetUser(user_1.user_id))
    self.assertEqual([user_1], fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_1.phone_number))
    self.assertEqual(user_2, fase_database.FaseDatabaseInterface.Get().GetUser(user_2.user_id))
    self.assertEqual([user_2], fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_2.phone_number))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetUser(user_2b.user_id))
    fase_database.FaseDatabaseInterface.Get().AddUser(user_2b)
    self.assertEqual(user_2b, fase_database.FaseDatabaseInterface.Get().GetUser(user_2b.user_id))
    self.assertEqual({user_2, user_2b},
                     set(fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_2b.phone_number)))



if __name__ == '__main__':
    unittest.main()
