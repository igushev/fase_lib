from server_util import config_util
from notes import database as notes_database


def GetNotesDatabase(config):
  return notes_database.DynamoDBNotesDatabase(
      region_name=config.get('dynamodb', 'region_name'))


notes_config = config_util.GetConfig('NOTES_CONFIG_FILENAME')
notes_database.NotesDatabaseInterface.Set(GetNotesDatabase(notes_config))
