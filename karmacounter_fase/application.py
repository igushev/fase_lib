import os

from fase_lib import fase
from fase_lib import fase_config
from fase_lib import fase_application

from karmacounter_fase import config as kc_config
from karmacounter_fase import service as kc_service


fase.Service.RegisterService(kc_service.KarmaCounter)

kc_config.Configurate(os.environ['KARMACOUNTER_FASE_CONFIG_FILENAME'])

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
