import os

from fase_test_fase import service as fase_test_service

from fase import fase
from fase import fase_config
from fase import fase_application


fase.Service.RegisterService(fase_test_service.FaseTestService)

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
