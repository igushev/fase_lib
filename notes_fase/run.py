import os
import time

from fase_lib import fase_run_util

FASE_SERVER_URL = 'http://notes-fase-env-test1.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'notes_fase/session_info'

IGNORE_SESSION_INFO = 'ignore'
RESET_FLAG = 'reset'
LOCAL_SERVER = 'local_server'


def CreateDatabase(server_url):
  from notes_fase import service as notes_service
  url = server_url + '/sendservicecommand'
  command_message = notes_service.CREATE_DB_COMMAND
  fase_run_util.SendCommand(url, command_message)


def SetupServer(dynamodb_url):
    from notes_fase import database as notes_database
    notes_database.NotesDatabaseInterface.Set(
        notes_database.DynamoDBNotesDatabase(endpoint_url=dynamodb_url, region_name=fase_run_util.DYNAMODB_REGION,
                                             aws_access_key_id='KeyId', aws_secret_access_key='AccessKey'))
    time.sleep(1)


def main(argv):
  arg_list = [arg[2:] for arg in argv[1:] if arg.startswith('--')]
  local_server = LOCAL_SERVER in arg_list
  if not local_server:
    session_info_filepath = (os.path.join(os.getcwd(), FASE_SESSION_INFO_FILENAME)
                             if IGNORE_SESSION_INFO not in arg_list else None)
    if RESET_FLAG in arg_list:
      os.remove(session_info_filepath)
    fase_run_util.RunClient(fase_server_url=FASE_SERVER_URL, session_info_filepath=session_info_filepath)
  else:
    import service as notes_service
    from fase_lib import fase
    fase.Service.RegisterService(notes_service.NotesService)

    server_info = fase_run_util.RunServer()
    SetupServer(dynamodb_url=server_info.dynamodb_url)
    CreateDatabase(server_url=server_info.server_url)
    fase_run_util.RunClient(fase_server_url=server_info.server_url)
    fase_run_util.StopServer(server_info)


if __name__ == '__main__':
  main(os.sys.argv)
