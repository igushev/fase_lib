import os

from fase_server import fase_run

FASE_SERVER_URL = 'http://hello-world-fase-env-test1.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'hello_world_fase/session_info'

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
    fase_run.RunClient(fase_server_url=FASE_SERVER_URL, session_info_filepath=session_info_filepath)
  else:
    from hello_world_fase import service as hello_world_service
    from fase import fase
    fase.Service.RegisterService(hello_world_service.HelloWorldService)

    server_info = fase_run.RunServer()
    fase_run.RunClient(fase_server_url=server_info.server_url)
    fase_run.StopServer(server_info)


if __name__ == '__main__':
  main(os.sys.argv)
