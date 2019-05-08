import os

from fase_lib import fase
from fase_lib import fase_config
from fase_lib import fase_application

from fase_test_fase import service as fase_test_service


fase.Service.RegisterService(fase_test_service.FaseTestService)

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
