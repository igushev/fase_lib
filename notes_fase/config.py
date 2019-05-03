from server_util import config_util

from notes_fase import database as notes_database
from notes_fase import service as notes_service


def GetNotesDatabase(config):
  return notes_database.DynamoDBNotesDatabase(
      tables_suffix=config.get('database', 'tables_suffix'),
      region_name=config.get('dynamodb', 'region_name'))


def ConfigService(config):
  if config.has_section('service'):
    if config.has_option('service', 'allow_deletedb'):
      notes_service.NotesService.allow_deletedb = bool(config.get('service', 'allow_deletedb'))


def Configurate(filename):
  notes_config = config_util.GetConfigByFilename(filename)
  notes_database.NotesDatabaseInterface.Set(GetNotesDatabase(notes_config))
  ConfigService(notes_config)
