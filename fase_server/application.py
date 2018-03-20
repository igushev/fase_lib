import os

from fase_server import fase_config
from fase_server import fase_http_server
# Register implementations
from fase_server import fase_pusher_impl
from fase_server import fase_sign_in_impl


application = fase_http_server.application

exec('import %s' % os.environ['FASE_SERVICE_MODULE'])

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000


def main(argv):
  fase_http_server.application.run(host=SERVER_HOST, port=SERVER_PORT)


if __name__ == '__main__':
  main(os.sys.argv)
