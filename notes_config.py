import config_util
import notes_database


def GetNotesDatabase(config):
  return notes_database.DynamoDBNotesDatabase(
      region_name=config.get('dynamodb', 'region_name'),
      endpoint_url=config.get('dynamodb', 'endpoint_url'),
      aws_access_key_id=config.get('dynamodb', 'aws_access_key_id'),
      aws_secret_access_key=config.get('dynamodb', 'aws_secret_access_key'))


notes_config = config_util.GetConfig('NOTES_CONFIG_FILENAME')
notes_database.NotesDatabaseInterface.Set(GetNotesDatabase(notes_config))
