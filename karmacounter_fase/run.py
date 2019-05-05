import os

from fase_server import fase_run

KARMACOUNTER_URL = 'http://karmacounter-env-test1.us-west-2.elasticbeanstalk.com/'
FASE_SERVER_URL = 'http://karmacounter-fase-env-test1.us-west-2.elasticbeanstalk.com'
FASE_SESSION_INFO_FILENAME = 'karmacounter_fase/session_info'

IGNORE_SESSION_INFO = 'ignore'
RESET_FLAG = 'reset'
LOCAL_SERVER = 'local_server'


def SetupClient(server_url):
  from karmacounter_fase import client as kc_client
  kc_client.KarmaCounterClient.Set(kc_client.KarmaCounterClient(server_url=server_url))


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
    from karmacounter_fase import service as kc_service 
    from fase import fase
    fase.Service.RegisterService(kc_service.KarmaCounter)

    server_info = fase_run.RunServer()
    SetupClient(KARMACOUNTER_URL)
    fase_run.RunClient(fase_server_url=server_info.server_url)
    fase_run.StopServer(server_info)


if __name__ == '__main__':
  main(os.sys.argv)
