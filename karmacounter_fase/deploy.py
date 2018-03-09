import os

from server_util import deploy_util


HOME_DIR_VAR_NAME = 'FASE_HOME'
DEPLOY_DIR_VAR_NAME = 'KARMACOUNTER_FASE_SERVER_DEPLOY_DIR'
KARMACOUNTER_VERSION_FILENAME = 'karmacounter_fase/version.txt'
FASE_VERSION_FILENAME = 'fase_server/fase_version.txt'
FILENAME_TEMPLATE = 'KarmaCounterFaseServer_KarmaCounter_%s_Fase_%s'

DEP_LIST = [
    'base_util',
    'fase',
    'fase_client',
    'fase_doc',
    'fase_model',
    'fase_server',
    'karmacounter_fase',
    'phonenumbers',
    'server_util',
]

MOVE_LIST = [
    ('fase_server/application.py', 'application.py'),
    ('fase_server/requirements.txt', 'requirements.txt')
]


def main(argv):
  assert len(argv) <= 2
  kc_position = int(argv[1]) if len(argv) == 2 else None

  home_dir = os.environ[HOME_DIR_VAR_NAME]
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  karmacounter_version = deploy_util.ReadAndUpdateVersion(KARMACOUNTER_VERSION_FILENAME, kc_position)
  fase_version = deploy_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME)
  filename = FILENAME_TEMPLATE % (karmacounter_version.replace('.', '_'), fase_version.replace('.', '_'))
  deploy_util.Deploy(home_dir, DEP_LIST, MOVE_LIST, deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
