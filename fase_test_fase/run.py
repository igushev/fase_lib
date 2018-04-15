import os
import signal

from fase_server import fase_run


FASE_SERVER_URL = 'http://fase-test-fase-env-test1.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'fase_test_fase/session_info'

IGNORE_SESSION_INFO = 'ignore'
RESET_FLAG = 'reset'
LOCAL_SERVER = 'local_server'

DYNAMODB_PORT = 8000
DYNAMODB_URL = 'http://localhost:%d'
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
SERVER_URL = 'http://localhost:%d'


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
    from fase_test_fase import service as fase_test_service
    dynamodb_process = fase_run.RunDatabase(dynamodb_port=DYNAMODB_PORT, dynamodb_url=DYNAMODB_URL % DYNAMODB_PORT)
    fase_run.RunServerThread(server_host=SERVER_HOST, server_port=SERVER_PORT)
    fase_run.CreateDatabase(server_url=SERVER_URL % SERVER_PORT)
    fase_run.RunClient(fase_server_url=SERVER_URL % SERVER_PORT)
    os.killpg(dynamodb_process.pid, signal.SIGKILL)


if __name__ == '__main__':
  main(os.sys.argv)
