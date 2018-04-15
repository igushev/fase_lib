import os

from server_util import deploy_util


HOME_DIR_VAR_NAME = 'FASE_HOME'
DEPLOY_DIR_VAR_NAME = 'FASE_TEST_FASE_SERVER_DEPLOY_DIR'
FASE_TEST_VERSION_FILENAME = 'fase_test_fase/version.txt'
FASE_VERSION_FILENAME = 'fase_server/fase_version.txt'
FILENAME_TEMPLATE = 'FaseTestFaseServer_FaseTest_%s_Fase_%s'

DEP_LIST = [
    'base_util',
    'fase',
    'fase_client',
    'fase_doc',
    'fase_model',
    'fase_server',
    'fase_test_fase',
    'phonenumbers',
    'server_util',
]

MOVE_LIST = [
    ('fase_server/application.py', 'application.py'),
    ('fase_server/requirements.txt', 'requirements.txt')
]


def main(argv):
  assert len(argv) <= 2
  fase_test_position = int(argv[1]) if len(argv) == 2 else None

  home_dir = os.environ[HOME_DIR_VAR_NAME]
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  fase_test_version = deploy_util.ReadAndUpdateVersion(FASE_TEST_VERSION_FILENAME, fase_test_position)
  fase_version = deploy_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME)
  filename = FILENAME_TEMPLATE % (fase_test_version.replace('.', '_'), fase_version.replace('.', '_'))
  deploy_util.Deploy(home_dir, DEP_LIST, MOVE_LIST, deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
