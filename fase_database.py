import boto3
from boto3.dynamodb.conditions import Key, Attr

import dynamodb_util
import fase
import fase_model
import singleton_util


@singleton_util.Singleton()
class FaseDatabaseInterface(object):

  def AddService(self, service, overwrite=False):
    raise NotImplemented()

  def GetService(self, session_id):
    raise NotImplemented()

  def AddScreen(self, screen, overwrite=False):
    raise NotImplemented()

  def GetScreen(self, session_id):
    raise NotImplemented()


class MockFaseDatabase(FaseDatabaseInterface):

  def __init__(self, service_list, screen_list, user_list):
    self.session_id_to_service = {
        service._session_id: service for service in service_list}
    self.session_id_to_screen = {
        screen._session_id: screen for screen in screen_list}
    self.user_id_to_user = {
        user.user_id: user for user in user_list}

  def AddService(self, service, overwrite=False):
    assert service._session_id not in self.session_id_to_service or overwrite
    self.session_id_to_service[service._session_id] = service

  def GetService(self, session_id):
    return self.session_id_to_service.get(session_id)

  def DeleteService(self, session_id):
    del self.session_id_to_service[session_id]

  def AddScreen(self, screen, overwrite=False):
    assert screen._session_id not in self.session_id_to_screen or overwrite
    self.session_id_to_screen[screen._session_id] = screen

  def GetScreen(self, session_id):
    return self.session_id_to_screen.get(session_id)

  def DeleteScreen(self, session_id):
    del self.session_id_to_screen[session_id]

  def AddUser(self, user, overwrite=False):
    assert user.user_id not in self.user_id_to_user or overwrite
    self.user_id_to_user[user.user_id] = user

  def GetUser(self, user_id):
    return self.user_id_to_user.get(user_id)

  def GetUserListByPhoneNumber(self, phone_number):
    user_list = [user for user in self.user_id_to_user.itervalues() if user.phone_number == phone_number]
    return user_list

  def GetSessionIdToService(self):
    return self.session_id_to_service
  
  def GetSessionIdToScreen(self):
    return self.session_id_to_screen
  
  def GetUserIdToUser(self):
    return self.user_id_to_user


class DynamoDBFaseDatabase(FaseDatabaseInterface):

  def __init__(self, **kwargs):
    self.dynamodb = boto3.client('dynamodb', **kwargs)

  def _GetServiceTableName(self):
    return 'Service'

  def _GetScreenTableName(self):
    return 'Screen'

  def _GetUserTableName(self):
    return 'User'

  def CreateTables(self):
    table_names_response = self.dynamodb.list_tables()
    table_names = table_names_response['TableNames']

    if self._GetServiceTableName() not in table_names:
      self.dynamodb.create_table(
          TableName=self._GetServiceTableName(),
          AttributeDefinitions=[
              {
                  'AttributeName': '_session_id',
                  'AttributeType': 'S'
              },
          ],
          KeySchema=[
              {
                  'AttributeName': '_session_id',
                  'KeyType': 'HASH'
              },
          ],
          ProvisionedThroughput={
              'ReadCapacityUnits': 10,
              'WriteCapacityUnits': 10
          }
      )    

    if self._GetScreenTableName() not in table_names:
      self.dynamodb.create_table(
          TableName=self._GetScreenTableName(),
          AttributeDefinitions=[
              {
                  'AttributeName': '_session_id',
                  'AttributeType': 'S'
              },
          ],
          KeySchema=[
              {
                  'AttributeName': '_session_id',
                  'KeyType': 'HASH'
              },
          ],
          ProvisionedThroughput={
              'ReadCapacityUnits': 10,
              'WriteCapacityUnits': 10
          }
      )    

    if self._GetUserTableName() not in table_names:
      self.dynamodb.create_table(
          TableName=self._GetUserTableName(),
          AttributeDefinitions=[
              {
                  'AttributeName': 'user_id',
                  'AttributeType': 'S'
              },
              {
                  'AttributeName': 'phone_number',
                  'AttributeType': 'S'
              },
              {
                  'AttributeName': 'datetime_added',
                  'AttributeType': 'S'
              },
          ],
          KeySchema=[
              {
                  'AttributeName': 'user_id',
                  'KeyType': 'HASH'
              },
          ],
          GlobalSecondaryIndexes=[
              {
                  'IndexName': 'phone_number_index',
                  'KeySchema': [
                      {
                          'AttributeName': 'phone_number',
                          'KeyType': 'HASH'
                      },
                      {
                          'AttributeName': 'datetime_added',
                          'KeyType': 'RANGE'
                      },
                  ],
                  'Projection': {
                      'ProjectionType': 'ALL',
                  },
                  'ProvisionedThroughput': {
                      'ReadCapacityUnits': 10,
                      'WriteCapacityUnits': 10
                  }
              },
          ],
          ProvisionedThroughput={
              'ReadCapacityUnits': 10,
              'WriteCapacityUnits': 10
          }
      )

  def AddService(self, service, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetServiceTableName(),
        Item=dynamodb_util.SimpleToItem(service.ToSimple()))

  def GetService(self, session_id):
    service_response = self.dynamodb.get_item(
        TableName=self._GetServiceTableName(),
        Key={
            '_session_id': dynamodb_util.SimpleToField(session_id),
            }
    )
    if 'Item' not in service_response:
      return None
    service = fase.Service.FromSimple(dynamodb_util.ItemToSimple(service_response['Item']))
    return service

  def DeleteService(self, session_id):
    self.dynamodb.delete_item(
        TableName=self._GetServiceTableName(),
        Key={
            '_session_id': dynamodb_util.SimpleToField(session_id),
            }
    )

  def AddScreen(self, screen, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetScreenTableName(),
        Item=dynamodb_util.SimpleToItem(screen.ToSimple()))

  def GetScreen(self, session_id):
    screen_response = self.dynamodb.get_item(
        TableName=self._GetScreenTableName(),
        Key={
            '_session_id': dynamodb_util.SimpleToField(session_id),
            }
    )
    if 'Item' not in screen_response:
      return None
    screen = fase.Screen.FromSimple(dynamodb_util.ItemToSimple(screen_response['Item']))
    return screen

  def DeleteScreen(self, session_id):
    self.dynamodb.delete_item(
        TableName=self._GetScreenTableName(),
        Key={
            '_session_id': dynamodb_util.SimpleToField(session_id),
            }
    )

  def AddUser(self, user, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetUserTableName(),
        Item=dynamodb_util.SimpleToItem(user.ToSimple()))

  def GetUser(self, user_id):
    user_response = self.dynamodb.get_item(
        TableName=self._GetUserTableName(),
        Key={
            'user_id': dynamodb_util.SimpleToField(user_id),
            }
    )
    if 'Item' not in user_response:
      return None
    user = fase_model.User.FromSimple(dynamodb_util.ItemToSimple(user_response['Item']))
    return user

  def GetUserListByPhoneNumber(self, phone_number):
    user_list_response = self.dynamodb.query(
        TableName=self._GetUserTableName(),
        IndexName='phone_number_index',
        KeyConditionExpression='phone_number = :phone_number',
        ExpressionAttributeValues={':phone_number': dynamodb_util.SimpleToField(phone_number)})
    user_list = [fase_model.User.FromSimple(dynamodb_util.ItemToSimple(user_item))
             for user_item in user_list_response['Items']]
    return user_list
