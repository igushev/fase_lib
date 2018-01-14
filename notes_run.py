import os

import fase_run


FASE_SERVER_URL = 'http://fasenotes-env.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILEPATH_VAR = 'FASE_NOTES_SESSION_INFO_FILEPATH'
RESET_FLAG = 'reset'


def main(argv):
  arg_list = [arg[2:] for arg in argv[1:] if arg.startswith('--')]
  session_info_filepath = os.environ.get(FASE_SESSION_INFO_FILEPATH_VAR, None)
  if RESET_FLAG in arg_list:
    os.remove(session_info_filepath)
  fase_run.Run(FASE_SERVER_URL, session_info_filepath=session_info_filepath)


if __name__ == '__main__':
  main(os.sys.argv)
