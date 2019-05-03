import os

from hello_world_fase import service as hello_world_service

from fase import fase
from fase import fase_config
from fase import fase_application


fase.Service.RegisterService(hello_world_service.HelloWorldService)

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
