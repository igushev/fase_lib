import os
import signal
import time

import fase_run


FASE_SERVER_URL = 'http://fasenotes-env.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'notes_session_info'
IGNORE_SESSION_INFO = 'ignore'
RESET_FLAG = 'reset'
LOCAL_SERVER = 'local_server'


def CreateDatabase(server_url):
  import notes
  url = server_url + '/sendservicecommand'
  command_message = notes.CREATE_DB_COMMAND
  fase_run.SendCommand(url, command_message)


def SetupServer():
    import notes_database
    notes_database.NotesDatabaseInterface.Set(
        notes_database.DynamoDBNotesDatabase(endpoint_url=fase_run.DYNAMODB_URL, region_name=fase_run.DYNAMODB_REGION,
                                             aws_access_key_id='KeyId', aws_secret_access_key='AccessKey'))
    time.sleep(1)
    CreateDatabase(fase_run.SERVER_URL)


def main(argv):
  arg_list = [arg[2:] for arg in argv[1:] if arg.startswith('--')]
  local_server = LOCAL_SERVER in arg_list
  if not local_server:
    session_info_filepath = (os.path.join(os.getcwd(), FASE_SESSION_INFO_FILENAME)
                             if IGNORE_SESSION_INFO not in arg_list else None)
    if RESET_FLAG in arg_list:
      os.remove(session_info_filepath)
    fase_run.RunClient(FASE_SERVER_URL, session_info_filepath=session_info_filepath)
  else:
    import notes
    dynamodb_process = fase_run.RunServerThread()
    SetupServer()
    fase_run.RunClient(fase_run.SERVER_URL)
    os.killpg(dynamodb_process.pid, signal.SIGKILL)


if __name__ == '__main__':
  main(os.sys.argv)
