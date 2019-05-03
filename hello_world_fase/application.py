import os

from hello_world_fase import service as hello_world_service

from fase import fase
from fase import fase_application

application = fase_application.application


fase.Service.RegisterService(hello_world_service.HelloWorldService)
fase_application.Configurate(os.environ['FASE_CONFIG_FILENAME'])
