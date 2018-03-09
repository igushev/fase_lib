import os

from server_util import deploy_util


HOME_DIR_VAR_NAME = 'FASE_HOME'
DEPLOY_DIR_VAR_NAME = 'HELLO_WORLD_FASE_SERVER_DEPLOY_DIR'
HELLO_WORLD_VERSION_FILENAME = 'hello_world_fase/version.txt'
FASE_VERSION_FILENAME = 'fase_server/fase_version.txt'
FILENAME_TEMPLATE = 'HelloWorldFaseServer_HelloWorld_%s_Fase_%s'

DEP_LIST = [
    'base_util',
    'fase',
    'fase_client',
    'fase_doc',
    'fase_model',
    'fase_server',
    'hello_world_fase',
    'phonenumbers',
    'server_util',
]

MOVE_LIST = [
    ('fase_server/application.py', 'application.py'),
    ('fase_server/requirements.txt', 'requirements.txt')
]


def main(argv):
  assert len(argv) <= 2
  hello_world_position = int(argv[1]) if len(argv) == 2 else None

  home_dir = os.environ[HOME_DIR_VAR_NAME]
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  hello_world_version = deploy_util.ReadAndUpdateVersion(HELLO_WORLD_VERSION_FILENAME, hello_world_position)
  fase_version = deploy_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME)
  filename = FILENAME_TEMPLATE % (hello_world_version.replace('.', '_'), fase_version.replace('.', '_'))
  deploy_util.Deploy(home_dir, DEP_LIST, MOVE_LIST, deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
