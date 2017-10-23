import fase_config

import notes_database


notes_config = fase_config.GetConfig('NOTES_CONFIG_FILENAME')
notes_database.NotesDatabaseInterface.Set(notes_database.NotesDatabaseInterface(
    fase_config.GetDatabaseConfig(notes_config), fase_config.GetDynamoDBConnection(notes_config)))
