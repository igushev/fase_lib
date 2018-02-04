import os
import signal

import fase_run


FASE_SERVER_URL = 'http://fasekarmacounter-env.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'KarmaCounter/session_info'
IGNORE_SESSION_INFO = 'ignore'
RESET_FLAG = 'reset'
LOCAL_SERVER = 'local_server'


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
    from KarmaCounter import service as kc_service 
    dynamodb_process = fase_run.RunServerThread()
    fase_run.RunClient(fase_run.SERVER_URL)
    os.killpg(dynamodb_process.pid, signal.SIGKILL)


if __name__ == '__main__':
  main(os.sys.argv)
