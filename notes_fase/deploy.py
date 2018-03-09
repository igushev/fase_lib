import os

from server_util import deploy_util


HOME_DIR_VAR_NAME = 'FASE_HOME'
DEPLOY_DIR_VAR_NAME = 'FASE_NOTES_SERVER_DEPLOY_DIR'
FASE_VERSION_FILENAME = 'fase_server/fase_version.txt'
NOTES_VERSION_FILENAME = 'notes_fase/version.txt'
FILENAME_TEMPLATE = 'FaseNotesServer_Fase_%s_Notes_%s'

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
    ('fase_server/application.py', 'application.py'),
    ('fase_server/requirements.txt', 'requirements.txt')
]


def main(argv):
  assert len(argv) <= 2
  notes_position = int(argv[1]) if len(argv) == 2 else None

  home_dir = os.environ[HOME_DIR_VAR_NAME]
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  fase_version = deploy_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME)
  notes_version = deploy_util.ReadAndUpdateVersion(NOTES_VERSION_FILENAME, notes_position)
  filename = FILENAME_TEMPLATE % (fase_version.replace('.', '_'), notes_version.replace('.', '_'))
  deploy_util.Deploy(home_dir, DEP_LIST, MOVE_LIST, deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
