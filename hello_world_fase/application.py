import os

import service as hello_world_service

import fase
import fase_config
import fase_application


fase.Service.RegisterService(hello_world_service.HelloWorldService)

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
