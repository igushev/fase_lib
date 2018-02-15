import os
import deploy_util

FASE_VERSION_FILENAME = 'fase_version.txt'
KC_VERSION_FILENAME = 'karmacounter/version.txt'
DEPLOY_DIR_VAR_NAME = 'FASE_KC_SERVER_DEPLOY_DIR'
FILENAME_TEMPLATE = 'FaseKCServer_Fase_%s_KC_%s'


def main(argv):
  assert len(argv) <= 2
  kc_position = int(argv[1]) if len(argv) == 2 else None

  fase_version = deploy_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME)
  kc_version = deploy_util.ReadAndUpdateVersion(KC_VERSION_FILENAME, kc_position)
  deploy_util.Clean()
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  filename = FILENAME_TEMPLATE % (fase_version.replace('.', '_'), kc_version.replace('.', '_'))
  deploy_util.Deploy(deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
