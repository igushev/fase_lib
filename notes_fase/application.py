import os

from notes_fase import config as notes_config
from notes_fase import service as notes_service

from fase import fase
from fase import fase_application

application = fase_application.application


fase.Service.RegisterService(notes_service.NotesService)
fase_application.Configurate(os.environ['FASE_CONFIG_FILENAME'])
notes_config.Configurate(os.environ['NOTES_CONFIG_FILENAME'])
