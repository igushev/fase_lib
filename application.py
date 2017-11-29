import os

import fase_config
import fase_http_server

application = fase_http_server.application

exec('import %s' % os.environ['FASE_SERVICE_MODULE'])

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000


def main(argv):
  fase_http_server.application.run(host=SERVER_HOST, port=SERVER_PORT)


if __name__ == '__main__':
  main(os.sys.argv)
