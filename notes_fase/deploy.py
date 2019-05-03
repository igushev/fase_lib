import os

from fase_server import fase_deploy
from notes_fase import service as notes_service
from server_util import deploy_util
from server_util import version_util


HOME_DIR_VAR_NAME = 'FASE_HOME'
DEPLOY_DIR_VAR_NAME = 'NOTES_FASE_SERVER_DEPLOY_DIR'
FILENAME_TEMPLATE = 'NotesFaseServer_Notes_%s_Fase_%s'

DEP_LIST = [
    'base_util',
    'fase',
    'fase_client',
    'fase_doc',
    'fase_model',
    'fase_server',
    'notes_fase',
    'phonenumbers',
    'server_util',
]

MOVE_LIST = [
    ('notes_fase/application.py', 'application.py'),
    ('notes_fase/requirements.txt', 'requirements.txt')
]


def main(argv):
  assert len(argv) <= 2
  notes_position = int(argv[1]) if len(argv) == 2 else None

  home_dir = os.environ[HOME_DIR_VAR_NAME]
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  notes_version = version_util.ReadAndUpdateVersion(notes_service.NOTES_VERSION_FILENAME, notes_position)
  fase_version = version_util.ReadAndUpdateVersion(fase_deploy.FASE_VERSION_FILENAME)
  filename = FILENAME_TEMPLATE % (notes_version.replace('.', '_'), fase_version.replace('.', '_'))
  deploy_util.Deploy(home_dir, DEP_LIST, MOVE_LIST, deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
