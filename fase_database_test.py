import datetime
import os
import signal
import subprocess
import unittest

import hello_world
import fase_database
import fase_model


DYNAMODB_CMD = (
    'java'
    ' -Djava.library.path=~/DynamoDBLocal/DynamoDBLocal_lib'
    ' -jar ~/DynamoDBLocal/DynamoDBLocal.jar -inMemory')


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

    service_1 = hello_world.HelloWorldService()
    screen_1 = service_1.OnStart()
    session_id_1 = service_1.GetSessionId()

    service_2 = hello_world.HelloWorldService()
    screen_2 = service_2.OnStart()
    text_name = screen_2.GetElement(id_='text_name_id') 
    text_name.Update('Edward Igushev')
    screen_2 = service_2.OnNextButton(screen_2, text_name)
    session_id_2 = service_2.GetSessionId()

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetService(session_id_1))
    fase_database.FaseDatabaseInterface.Get().AddService(service_1)
    self.assertEqual(service_1, fase_database.FaseDatabaseInterface.Get().GetService(session_id_1))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetService(session_id_2))
    fase_database.FaseDatabaseInterface.Get().AddService(service_2)
    self.assertEqual(service_1, fase_database.FaseDatabaseInterface.Get().GetService(session_id_1))
    self.assertEqual(service_2, fase_database.FaseDatabaseInterface.Get().GetService(session_id_2))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetScreen(session_id_1))
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen_1)
    self.assertEqual(screen_1, fase_database.FaseDatabaseInterface.Get().GetScreen(session_id_1))

    self.assertIsNone(fase_database.FaseDatabaseInterface.Get().GetScreen(session_id_2))
    fase_database.FaseDatabaseInterface.Get().AddScreen(screen_2)
    self.assertEqual(screen_1, fase_database.FaseDatabaseInterface.Get().GetScreen(session_id_1))
    self.assertEqual(screen_2, fase_database.FaseDatabaseInterface.Get().GetScreen(session_id_2))
    
    user_1 = fase_model.User(user_id='321',
                             phone_number='+13216549870',
                             first_name='Edward',
                             last_name='Igushev',
                             datetime_added=datetime.datetime.now())    
    user_2 = fase_model.User(user_id='987',
                             phone_number='+19876543210',
                             first_name='Edward Junior',
                             last_name='Igushev',
                             datetime_added=datetime.datetime.now())    
    user_2b = fase_model.User(user_id='987b',
                             phone_number='+19876543210',
                             first_name='Edward Junior',
                             last_name='Igushev (One more account)',
                             datetime_added=datetime.datetime.now())    

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
    self.assertEqual([user_2, user_2b],
                     fase_database.FaseDatabaseInterface.Get().GetUserListByPhoneNumber(user_2b.phone_number))



if __name__ == '__main__':
    unittest.main()
