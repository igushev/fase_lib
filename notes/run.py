import os
import signal
import time

from fase_server import fase_run


FASE_SERVER_URL = 'http://fasenotes-env.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'notes/session_info'

IGNORE_SESSION_INFO = 'ignore'
RESET_FLAG = 'reset'
LOCAL_SERVER = 'local_server'

DYNAMODB_PORT = 8000
DYNAMODB_URL = 'http://localhost:%d'
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
SERVER_URL = 'http://localhost:%d'


def CreateDatabase(server_url):
  from notes import service as notes_service
  url = server_url + '/sendservicecommand'
  command_message = notes_service.CREATE_DB_COMMAND
  fase_run.SendCommand(url, command_message)


def SetupServer(dynamodb_url):
    from notes import database as notes_database
    notes_database.NotesDatabaseInterface.Set(
        notes_database.DynamoDBNotesDatabase(endpoint_url=dynamodb_url, region_name=fase_run.DYNAMODB_REGION,
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
    fase_run.RunClient(fase_server_url=FASE_SERVER_URL, session_info_filepath=session_info_filepath)
  else:
    from notes import service as notes_service
    dynamodb_process = fase_run.RunDatabase(dynamodb_port=DYNAMODB_PORT, dynamodb_url=DYNAMODB_URL % DYNAMODB_PORT)
    fase_run.RunServerThread(server_host=SERVER_HOST, server_port=SERVER_PORT)
    fase_run.CreateDatabase(server_url=SERVER_URL % SERVER_PORT)
    SetupServer(DYNAMODB_URL % DYNAMODB_PORT)
    CreateDatabase(SERVER_URL % SERVER_PORT)
    fase_run.RunClient(fase_server_url=SERVER_URL % SERVER_PORT)
    os.killpg(dynamodb_process.pid, signal.SIGKILL)


if __name__ == '__main__':
  main(os.sys.argv)
