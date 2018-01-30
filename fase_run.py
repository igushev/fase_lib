import functools
import logging
import subprocess
import threading
import time
import os

import requests

import activation_code_generator
import fase_database
import fase_http_server
import sms_sender
import fase_model
import fase_server
import fase_client
import fase_tk_ui_imp
import fase_ui
import fase_http_client


DYNAMODB_CMD = (
    'java'
    ' -Djava.library.path=~/DynamoDBLocal/DynamoDBLocal_lib'
    ' -jar ~/DynamoDBLocal/DynamoDBLocal.jar -inMemory')

DYNAMODB_URL = 'http://localhost:8000'
DYNAMODB_REGION = 'us-west-2' 
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
SERVER_URL = 'http://localhost:5000'


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


def RunServerThread():
  dynamodb_process = (
      subprocess.Popen(DYNAMODB_CMD, shell=True, preexec_fn=os.setsid))
  fase_database.FaseDatabaseInterface.Set(
      fase_database.DynamoDBFaseDatabase(endpoint_url=DYNAMODB_URL, region_name=DYNAMODB_REGION,
                                         aws_access_key_id='KeyId', aws_secret_access_key='AccessKey'))
  activation_code_generator.ActivationCodeGenerator.Set(activation_code_generator.ActivationCodeGenerator())
  sms_sender.SMSSender.Set(sms_sender.SMSSender(sms_service_provider=sms_sender.PrintSMSServiceProvider()))
  fase_server.FaseServer.Set(fase_server.FaseServer())
  server_thread = threading.Thread(target=functools.partial(
      fase_http_server.application.run, host=SERVER_HOST, port=SERVER_PORT))
  server_thread.daemon = True
  server_thread.start()
  time.sleep(1)
  CreateDatabase(SERVER_URL)
  return dynamodb_process


def RunClient(fase_server_url, session_info_filepath=None):
  http_client = fase_http_client.FaseHTTPClient(fase_server_url)
  ui_imp = fase_tk_ui_imp.FaseTkUIImp()
  ui = fase_ui.FaseUI(ui_imp)
  client = fase_client.FaseClient(http_client, ui, session_info_filepath=session_info_filepath)
  client.Run()
