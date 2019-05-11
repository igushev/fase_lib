"""Fase Application."""


from fase_lib.fase_server import fase_http_server
# Register implementations
from fase_lib.fase_server import fase_config_impl
from fase_lib.fase_server import fase_pusher_impl
from fase_lib.fase_server import fase_sign_in_impl

# Reassign this variable into application.py of end application.
application = fase_http_server.application
