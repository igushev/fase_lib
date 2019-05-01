import os

from fase_server import fase_config
from fase_server import fase_http_server
# Register implementations
from fase_server import fase_pusher_impl
from fase_server import fase_sign_in_impl

application = fase_http_server.application

exec('import %s' % os.environ['FASE_SERVICE_MODULE'])

fase_config.FaseConfig(os.environ['FASE_CONFIG_FILENAME'])

def main(argv):
  fase_http_server.Run()


if __name__ == '__main__':
  main(os.sys.argv)
