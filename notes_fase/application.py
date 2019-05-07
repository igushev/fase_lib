import os

from fase_lib import fase
from fase_lib import fase_config
from fase_lib import fase_application

from notes_fase import config as notes_config
from notes_fase import service as notes_service


fase.Service.RegisterService(notes_service.NotesService)

notes_config.Configurate(os.environ['NOTES_CONFIG_FILENAME'])

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
