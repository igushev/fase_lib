import os

from fase_test_fase import service as fase_test_service

import fase
import fase_config
import fase_application


fase.Service.RegisterService(fase_test_service.FaseTestService)

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
