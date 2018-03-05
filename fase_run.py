import functools
import logging
import subprocess
import tempfile
import threading
import time
import os

import requests

from server_util import activation_code_generator
from fase_server import fase_database
from fase_server import fase_http_server
from server_util import sms_sender
import fase_model
from fase_server import fase_server
from fase_client import fase_client
from fase_client import fase_resource_manager
from fase_client import fase_tk_ui_imp
from fase_client import fase_ui
from fase_client import fase_http_client


DYNAMODB_CMD = (
    'java'
    ' -Djava.library.path=~/DynamoDBLocal/DynamoDBLocal_lib'
    ' -jar ~/DynamoDBLocal/DynamoDBLocal.jar -inMemory -port %d')
DYNAMODB_REGION = 'us-west-2' 


def AssertStatus(http_response):
  if http_response.status_code != requests.codes.ok:
    logging.error(http_response.text)
    http_response.raise_for_status()


def SendCommand(url, command_message):
  command = fase_model.Command(command=command_message)
  command_simple = command.ToSimple()
  http_response = requests.post(url, json=command_simple)
  AssertStatus(http_response)
  status_simple = http_response.json()
  status = fase_model.Status.FromSimple(status_simple)
  print(status.message)


def CreateDatabase(server_url):
  url = server_url + '/sendinternalcommand'
  command_message = fase_server.CREATE_DB_COMMAND
  SendCommand(url, command_message)


def RunDatabase(dynamodb_port, dynamodb_url):
  dynamodb_process = (
      subprocess.Popen(DYNAMODB_CMD % dynamodb_port, shell=True, preexec_fn=os.setsid))
  fase_database.FaseDatabaseInterface.Set(
      fase_database.DynamoDBFaseDatabase(endpoint_url=dynamodb_url, region_name=DYNAMODB_REGION,
                                         aws_access_key_id='KeyId', aws_secret_access_key='AccessKey'))
  return dynamodb_process


def RunServerThread(server_host, server_port):
  activation_code_generator.ActivationCodeGenerator.Set(activation_code_generator.ActivationCodeGenerator())
  sms_sender.SMSSender.Set(sms_sender.SMSSender(sms_service_provider=sms_sender.PrintSMSServiceProvider()))
  fase_server.FaseServer.Set(fase_server.FaseServer())
  server_thread = threading.Thread(target=functools.partial(
      fase_http_server.application.run, host=server_host, port=server_port))
  server_thread.daemon = True
  server_thread.start()
  time.sleep(1)


def RunClient(fase_server_url, session_info_filepath=None):
  http_client = fase_http_client.FaseHTTPClient(fase_server_url)
  ui_imp = fase_tk_ui_imp.FaseTkUIImp()
  ui = fase_ui.FaseUI(ui_imp)
  resource_dir = tempfile.mkdtemp()
  resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
  client = fase_client.FaseClient(http_client, ui, resource_manager, session_info_filepath=session_info_filepath)
  client.Run()
