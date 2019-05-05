import os

from server_util import version_util


FASE_VERSION_FILENAME = 'fase_server/fase_version.txt'


def main(argv):
  assert len(argv) <= 2
  update_position = int(argv[1]) if len(argv) == 2 else None
  version_util.ReadAndUpdateVersion(FASE_VERSION_FILENAME, update_position)


if __name__ == '__main__':
  main(os.sys.argv)
