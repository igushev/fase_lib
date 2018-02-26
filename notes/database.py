import boto3
from boto3.dynamodb.conditions import Key, Attr

import dynamodb_util
import singleton_util

from notes import model as notes_model


@singleton_util.Singleton()
class NotesDatabaseInterface(object):

  def GetUserNotes(self, user_id):
    raise NotImplemented()


class MockNotesDatabase(NotesDatabaseInterface):

  def __init__(self, note_list):
    self.note_id_note = {note.note_id: note for note in note_list}

  def CreateDatabase(self):
    pass

  def DeleteDatabase(self):
    pass

  def GetUserNotes(self, user_id):
    return [note for note in self.note_id_note.values() if note.user_id == user_id]

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
    return 'fase_notes'

  def CreateDatabase(self):
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
                  'IndexName': 'user_id_datetime_index',
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

  def DeleteDatabase(self):
    self.dynamodb.delete_table(TableName=self._GetNotesTableName())

  def GetUserNotes(self, user_id):
    notes_response = self.dynamodb.query(
        TableName=self._GetNotesTableName(),
        IndexName='user_id_datetime_index',
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues={':user_id': dynamodb_util.SimpleToField(user_id)})
    notes = [notes_model.Note.FromSimple(dynamodb_util.ItemToSimple(note_item))
             for note_item in notes_response['Items']]
    return notes

  def AddNote(self, note, overwrite=False):
    self.dynamodb.put_item(
        TableName=self._GetNotesTableName(),
        Item=dynamodb_util.SimpleToItem(note.ToSimple()))

  def GetNote(self, note_id):
    note_response = self.dynamodb.get_item(
        TableName=self._GetNotesTableName(),
        Key={
            'note_id': dynamodb_util.SimpleToField(note_id),
            }
    )
    if 'Item' not in note_response:
      return None
    note = notes_model.Note.FromSimple(dynamodb_util.ItemToSimple(note_response['Item']))
    return note

  def DeleteNote(self, note_id):
    self.dynamodb.delete_item(
        TableName=self._GetNotesTableName(),
        Key={
            'note_id': dynamodb_util.SimpleToField(note_id),
            }
    )
