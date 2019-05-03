import os

from karmacounter_fase import config as kc_config
from karmacounter_fase import service as kc_service

from fase import fase
from fase import fase_application

application = fase_application.application


fase.Service.RegisterService(kc_service.KarmaCounter)
fase_application.Configurate(os.environ['FASE_CONFIG_FILENAME'])
kc_config.Configurate(os.environ['KARMACOUNTER_FASE_CONFIG_FILENAME'])