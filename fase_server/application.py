import os

from server_util import resource_manager

from fase_server import fase_config
from fase_server import fase_http_server
from fase_server import fase_resource
# Register implementations
from fase_server import fase_pusher_impl
from fase_server import fase_sign_in_impl


application = fase_http_server.application

exec('import %s' % os.environ['FASE_SERVICE_MODULE'])

resource_manager.ResourceManager.Set(resource_manager.ResourceManager(fase_resource.GetResourceDir()))

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000


def main(argv):
  fase_http_server.application.run(host=SERVER_HOST, port=SERVER_PORT)


if __name__ == '__main__':
  main(os.sys.argv)
