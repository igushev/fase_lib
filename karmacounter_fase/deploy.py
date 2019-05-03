import os

from fase_server import fase_deploy
from karmacounter_fase import service as kc_service
from server_util import deploy_util
from server_util import version_util


HOME_DIR_VAR_NAME = 'FASE_HOME'
DEPLOY_DIR_VAR_NAME = 'KARMACOUNTER_FASE_SERVER_DEPLOY_DIR'
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
    ('karmacounter_fase/application.py', 'application.py'),
    ('karmacounter_fase/requirements.txt', 'requirements.txt')
]


def main(argv):
  assert len(argv) <= 2
  kc_position = int(argv[1]) if len(argv) == 2 else None

  home_dir = os.environ[HOME_DIR_VAR_NAME]
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  karmacounter_version = version_util.ReadAndUpdateVersion(kc_service.KARMACOUNTER_VERSION_FILENAME, kc_position)
  fase_version = version_util.ReadAndUpdateVersion(fase_deploy.FASE_VERSION_FILENAME)
  filename = FILENAME_TEMPLATE % (karmacounter_version.replace('.', '_'), fase_version.replace('.', '_'))
  deploy_util.Deploy(home_dir, DEP_LIST, MOVE_LIST, deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
