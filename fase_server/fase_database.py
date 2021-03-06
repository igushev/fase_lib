import boto3
from boto3.dynamodb.conditions import Key, Attr

from fase_lib import fase
from fase_lib.base_util import singleton_util
from fase_lib.server_util import dynamodb_util
from fase_lib.fase_model import fase_model


@singleton_util.Singleton()
class FaseDatabaseInterface(object):

  def AddServiceProg(self, service_prog, overwrite=False):
    raise NotImplemented()
  def GetServiceProg(self, session_id):
    raise NotImplemented()

  def AddScreenProg(self, screen_prog, overwrite=False):
    raise NotImplemented()
  def GetScreenProg(self, session_id):
    raise NotImplemented()


class MockFaseDatabase(FaseDatabaseInterface):

  def __init__(self, service_prog_list, screen_prog_list, user_list):
    self.session_id_to_service_prog = {service_prog.session_id: service_prog for service_prog in service_prog_list}
    self.session_id_to_screen_prog = {screen_prog.session_id: screen_prog for screen_prog in screen_prog_list}
    self.user_id_to_user = {user.user_id: user for user in user_list}

  def CreateDatabase(self):
    pass

  def DeleteDatabase(self):
    pass

  def AddServiceProg(self, service_prog, overwrite=False):
    assert service_prog.session_id not in self.session_id_to_service_prog or overwrite
    self.session_id_to_service_prog[service_prog.session_id] = service_prog

  def GetServiceProg(self, session_id):
    return self.session_id_to_service_prog.get(session_id)

  def DeleteServiceProg(self, session_id):
    del self.session_id_to_service_prog[session_id]

  def AddScreenProg(self, screen_prog, overwrite=False):
    assert screen_prog.session_id not in self.session_id_to_screen_prog or overwrite
    self.session_id_to_screen_prog[screen_prog.session_id] = screen_prog

  def GetScreenProg(self, session_id):
    return self.session_id_to_screen_prog.get(session_id)

  def DeleteScreenProg(self, session_id):
    del self.session_id_to_screen_prog[session_id]

  def AddUser(self, user, overwrite=False):
    assert user.user_id not in self.user_id_to_user or overwrite
    self.user_id_to_user[user.user_id] = user

  def GetUser(self, user_id):
    return self.user_id_to_user.get(user_id)

  def GetUserListByPhoneNumber(self, phone_number):
    user_list = [user for user in self.user_id_to_user.values() if user.phone_number == phone_number]
    return user_list

  def GetSessionIdToServiceProg(self):
    return self.session_id_to_service_prog
  
  def GetSessionIdToScreenProg(self):
    return self.session_id_to_screen_prog
  
  def GetUserIdToUser(self):
    return self.user_id_to_user


class DynamoDBFaseDatabase(FaseDatabaseInterface):

  def __init__(self, tables_suffix=None, **kwargs):
    self.tables_suffix = tables_suffix or ''
    self.dynamodb = boto3.client('dynamodb', **kwargs)

  def _GetServiceProgTableName(self):
    return 'fase_service_prog%s' % self.tables_suffix

  def _GetScreenProgTableName(self):
    return 'fase_screen_prog%s' % self.tables_suffix

  def _GetUserTableName(self):
    return 'fase_user%s' % self.tables_suffix

  @staticmethod
  def GetTableNameList():
    return ['fase_service_prog', 'fase_screen_prog', 'fase_user']

  def CreateDatabase(self):
    table_names_response = self.dynamodb.list_tables()
    table_names = table_names_response['TableNames']

    if self._GetServiceProgTableName() not in table_names:
      self.dynamodb.create_table(
          TableName=self._GetServiceProgTableName(),
          AttributeDefinitions=[
              {
                  'AttributeName': 'session_id',
                  'AttributeType': 'S'
              },
          ],
          KeySchema=[
              {
                  'AttributeName': 'session_id',
                  'KeyType': 'HASH'
              },
          ],
          ProvisionedThroughput={
              'ReadCapacityUnits': 10,
              'WriteCapacityUnits': 10
          }
      )    

    if self._GetScreenProgTableName() not in table_names:
      self.dynamodb.create_table(
          TableName=self._GetScreenProgTableName(),
          AttributeDefinitions=[
              {
                  'AttributeName': 'session_id',
                  'AttributeType': 'S'
              },
          ],
          KeySchema=[
              {
                  'AttributeName': 'session_id',
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

  def DeleteDatabase(self):
    self.dynamodb.delete_table(TableName=self._GetServiceProgTableName())
    self.dynamodb.delete_table(TableName=self._GetScreenProgTableName())
    self.dynamodb.delete_table(TableName=self._GetUserTableName())

  def AddServiceProg(self, service_prog, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetServiceProgTableName(),
        Item=dynamodb_util.SimpleToItem(service_prog.ToSimple()))

  def GetServiceProg(self, session_id):
    service_prog_response = self.dynamodb.get_item(
        TableName=self._GetServiceProgTableName(),
        Key={
            'session_id': dynamodb_util.SimpleToField(session_id),
            }
    )
    if 'Item' not in service_prog_response:
      return None
    service_prog = fase_model.ServiceProg.FromSimple(dynamodb_util.ItemToSimple(service_prog_response['Item']))
    return service_prog

  def DeleteServiceProg(self, session_id):
    self.dynamodb.delete_item(
        TableName=self._GetServiceProgTableName(),
        Key={
            'session_id': dynamodb_util.SimpleToField(session_id),
            }
    )

  def AddScreenProg(self, screen_prog, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetScreenProgTableName(),
        Item=dynamodb_util.SimpleToItem(screen_prog.ToSimple()))

  def GetScreenProg(self, session_id):
    screen_prog_response = self.dynamodb.get_item(
        TableName=self._GetScreenProgTableName(),
        Key={
            'session_id': dynamodb_util.SimpleToField(session_id),
            }
    )
    if 'Item' not in screen_prog_response:
      return None
    screen_prog = fase_model.ScreenProg.FromSimple(dynamodb_util.ItemToSimple(screen_prog_response['Item']))
    return screen_prog

  def DeleteScreenProg(self, session_id):
    self.dynamodb.delete_item(
        TableName=self._GetScreenProgTableName(),
        Key={
            'session_id': dynamodb_util.SimpleToField(session_id),
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
    user = fase.User.FromSimple(dynamodb_util.ItemToSimple(user_response['Item']))
    return user

  def GetUserListByPhoneNumber(self, phone_number):
    user_list_response = self.dynamodb.query(
        TableName=self._GetUserTableName(),
        IndexName='phone_number_index',
        KeyConditionExpression='phone_number = :phone_number',
        ExpressionAttributeValues={':phone_number': dynamodb_util.SimpleToField(phone_number)})
    user_list = [fase.User.FromSimple(dynamodb_util.ItemToSimple(user_item))
             for user_item in user_list_response['Items']]
    return user_list
