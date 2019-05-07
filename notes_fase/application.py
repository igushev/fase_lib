import os

from notes_fase import config as notes_config
from notes_fase import service as notes_service

import fase
import fase_config
import fase_application


fase.Service.RegisterService(notes_service.NotesService)

notes_config.Configurate(os.environ['NOTES_CONFIG_FILENAME'])

fase_config.Configurate(os.environ['FASE_CONFIG_FILENAME'])

application = fase_application.application
