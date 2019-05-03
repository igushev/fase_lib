from fase_server import fase_http_server
# Register implementations
from fase_server import fase_config_impl
from fase_server import fase_pusher_impl
from fase_server import fase_sign_in_impl

application = fase_http_server.application
