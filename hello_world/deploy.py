import os
from server_util import deploy_util

FASE_VERSION_FILENAME = 'fase_server/fase_version.txt'
HELLO_WORLD_VERSION_FILENAME = 'hello_world/version.txt'
DEPLOY_DIR_VAR_NAME = 'FASE_HELLO_WORLD_SERVER_DEPLOY_DIR'
FILENAME_TEMPLATE = 'FaseHelloWorldServer_Fase_%s_HelloWorld_%s'


def main(argv):
  assert len(argv) <= 2
  hello_world_position = int(argv[1]) if len(argv) == 2 else None

  fase_version = deploy_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME)
  hello_world_version = deploy_util.ReadAndUpdateVersion(HELLO_WORLD_VERSION_FILENAME, hello_world_position)
  deploy_util.Clean()
  deploy_dir = os.environ[DEPLOY_DIR_VAR_NAME]
  assert deploy_dir, '%s must be set!' % DEPLOY_DIR_VAR_NAME 
  filename = FILENAME_TEMPLATE % (fase_version.replace('.', '_'), hello_world_version.replace('.', '_'))
  deploy_util.Deploy(deploy_dir, filename)


if __name__ == '__main__':
  main(os.sys.argv)
