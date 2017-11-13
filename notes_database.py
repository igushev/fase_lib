import boto3
from boto3.dynamodb.conditions import Key, Attr

import notes_model
import singleton_util


def _SimpleToItem(simple):
  if isinstance(simple, list):
    return {'L': [_SimpleToItem(nested_simple) for nested_simple in simple]}
  elif isinstance(simple, dict):
    return {'M': {nested_key: _SimpleToItem(nested_simple) for nested_key, nested_simple in simple.iteritems()}}
  elif isinstance(simple, str):
    return {'S': simple}
  elif isinstance(simple, bool):
    return {'BOOL': simple}
  elif isinstance(simple, (float, int)):
    return {'N': str(simple)}
  elif simple is None:
    return {'NULL': True}
  else:
    return TypeError('Unsorted type: %s' % type(simple))


def SimpleToItem(simple):
  return {nested_key: _SimpleToItem(nested_simple) for nested_key, nested_simple in simple.iteritems()}


def _ItemToSimple(type_item):
  assert isinstance(type_item, dict)
  assert len(type_item) == 1
  type_, item = list(type_item.iteritems())[0]
  if type_ == 'L':
    return [_ItemToSimple(nested_type, nested_item) for nested_type, nested_item in item]
  elif type_ == 'M':
    return {nested_key: _ItemToSimple(nested_type, nested_item)
            for nested_key, (nested_type, nested_item) in item.iteritems()}
  elif type_ == 'S':
    return item
  elif type_ == 'BOOL':
    return item
  elif type_ == 'N':
    return float(item)
  elif type_ == 'NULL':
    assert item is True
    return None
  else:
    return TypeError('Unsorted type: %s' % type_)


def ItemToSimple(item):
  return {nested_key: _ItemToSimple(nested_type_item) for nested_key, nested_type_item in item.iteritems()} 


@singleton_util.Singleton()
class NotesDatabaseInterface(object):

  def GetUserNotes(self, user_id):
    raise NotImplemented()


class MockNotesDatabase(NotesDatabaseInterface):

  def __init__(self, note_list):
    self.note_id_note = {note.note_id: note for note in note_list}

  def GetUserNotes(self, user_id):
    return [note for note in self.note_id_note.itervalues() if note.user_id == user_id]

  def AddNote(self, note, overwrite=False):
    assert note.note_id not in self.note_id_note or overwrite
    self.note_id_note[note.note_id] = note

  def GetNote(self, note_id):
    return self.note_id_note[note_id]

  def DeleteNote(self, note_id):
    del self.note_id_note[note_id]



class DynamoDBNotesDatabase(NotesDatabaseInterface):

  def __init__(self, **kwargs):
    self.dynamodb = boto3.client('dynamodb', **kwargs)

  def _GetNotesTableName(self):
    return 'Notes'

  def CreateTables(self):
    table_names_response = self.dynamodb.list_tables()
    table_names = table_names_response['TableNames']
    
    if self._GetNotesTableName() not in table_names:
      self.dynamodb.create_table(
          TableName=self._GetNotesTableName(),
          AttributeDefinitions=[
              {
                  'AttributeName': 'note_id',
                  'AttributeType': 'S'
              },
              {
                  'AttributeName': 'user_id',
                  'AttributeType': 'S'
              },
              {
                  'AttributeName': 'datetime',
                  'AttributeType': 'S'
              },
          ],
          KeySchema=[
              {
                  'AttributeName': 'note_id',
                  'KeyType': 'HASH'
              },
          ],
          GlobalSecondaryIndexes=[
              {
                  'IndexName': 'user_id_datetime',
                  'KeySchema': [
                      {
                          'AttributeName': 'user_id',
                          'KeyType': 'HASH'
                      },
                      {
                          'AttributeName': 'datetime',
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

  def GetUserNotes(self, user_id):
    notes_response = self.dynamodb.query(
        TableName=self._GetNotesTableName(),
        IndexName='user_id_datetime',
        KeyConditionExpression='user_id = :user_id', ExpressionAttributeValues={':user_id': _SimpleToItem(user_id)})
    notes = [notes_model.Note.FromSimple(ItemToSimple(note_item)) for note_item in notes_response['Items']]
    return notes

  def AddNote(self, note, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetNotesTableName(),
        Item=SimpleToItem(note.ToSimple()))

  def GetNote(self, note_id):
    note_response = self.dynamodb.get_item(
        TableName=self._GetNotesTableName(),
        Key={
            'note_id': _SimpleToItem(note_id),
            }
    )
    note = notes_model.Note.FromSimple(ItemToSimple(note_response['Item']))
    return note

  def DeleteNote(self, note_id):
    self.dynamodb.delete_item(
        TableName=self._GetNotesTableName(),
        Key={
            'note_id': _SimpleToItem(note_id),
            }
    )
