import logging
import traceback
import os
import sys

from flask import Flask, request, jsonify, send_file

import fase
import fase_model
from json_util import json_util

try:
  from . import fase_sign_in_impl
  from . import fase_server
except SystemError:  
  import fase_sign_in_impl
  import fase_server


application = Flask(__name__)
application.secret_key = 'fase_flask_secret_key'

STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_ERROR = 500


def CleanSimple(simple):
  if isinstance(simple, list):
    return [CleanSimple(nested_simple) for nested_simple in simple]
  elif isinstance(simple, dict):
    clean_simple = {}
    for nested_key, nested_simple in simple.items():
      if nested_key in [fase.ON_CLICK_METHOD, fase.ON_PICK_METHOD, fase.ON_REFRESH_METHOD, fase.ON_MORE_METHOD]:
        clean_simple[nested_key] = (
            json_util.JSONFunction().ToSimple(fase.FunctionPlaceholder) if nested_simple is not None else None)
      elif nested_key == json_util.MODULE_FIELD and nested_simple == fase_sign_in_impl.__name__:
        clean_simple[nested_key] = fase.__name__
      elif (nested_key == json_util.CLASS_FIELD and (nested_simple == fase_sign_in_impl.FaseSignInButton.__name__ or
                                                     nested_simple == fase_sign_in_impl.FaseSignOutButton.__name__)):
        clean_simple[nested_key] = fase.Button.__name__
      else:
        clean_simple[nested_key] = CleanSimple(nested_simple)
    return clean_simple
  else:
    return simple


def SafeCall(func, *args, **kwargs):
  try:
    res = func(*args, **kwargs)
    return res.ToSimple(), STATUS_OK
  except fase_server.BadRequestException as bad_request_exception:
    return bad_request_exception.BadRequest().ToSimple(), STATUS_BAD_REQUEST
  except Exception as e:
    logging.error(type(e))
    logging.error(str(e))
    logging.error(str(traceback.format_exc()))
    return fase_model.Status(str(traceback.format_exc())).ToSimple(), STATUS_ERROR


@application.route('/sendinternalcommand', methods=['POST', 'OPTIONS'])
def sendinternalcommand():
  command_simple = request.get_json(force=True) 
  command = fase_model.Command.FromSimple(command_simple)
  status_simple, code = SafeCall(fase_server.FaseServer.Get().SendInternalCommand, command)
  return jsonify(**status_simple), code


@application.route('/sendservicecommand', methods=['POST', 'OPTIONS'])
def sendservicecommand():
  command_simple = request.get_json(force=True) 
  command = fase_model.Command.FromSimple(command_simple)
  status_simple, code = SafeCall(fase_server.FaseServer.Get().SendServiceCommand, command)
  return jsonify(**status_simple), code


@application.route('/getservice', methods=['POST', 'OPTIONS'])
def getservice():
  device_simple = request.get_json(force=True) 
  device = fase_model.Device.FromSimple(device_simple)
  response_simple, code = SafeCall(fase_server.FaseServer.Get().GetService, device)
  response_simple = CleanSimple(response_simple)
  return jsonify(**response_simple), code


@application.route('/getscreen', methods=['POST', 'OPTIONS'])
def getscreen():
  session_info = fase_model.SessionInfo(session_id=request.headers.get('session_id', None))
  device_simple = request.get_json(force=True) 
  device = fase_model.Device.FromSimple(device_simple)
  response_simple, code = SafeCall(fase_server.FaseServer.Get().GetScreen, device, session_info)
  response_simple = CleanSimple(response_simple)
  return jsonify(**response_simple), code


@application.route('/screenupdate', methods=['POST', 'OPTIONS'])
def screenupdate():
  session_info = fase_model.SessionInfo(session_id=request.headers.get('session_id', None))
  screen_info = fase_model.ScreenInfo(screen_id=request.headers.get('screen_id', None))
  screen_update_simple = request.get_json(force=True) 
  screen_update = fase_model.ScreenUpdate.FromSimple(screen_update_simple)
  response_simple, code = SafeCall(fase_server.FaseServer.Get().ScreenUpdate, screen_update, session_info, screen_info)
  response_simple = CleanSimple(response_simple)
  return jsonify(**response_simple), code


@application.route('/elementcallback', methods=['POST', 'OPTIONS'])
def elementcallback():
  session_info = fase_model.SessionInfo(session_id=request.headers.get('session_id', None))
  screen_info = fase_model.ScreenInfo(screen_id=request.headers.get('screen_id', None))
  element_callback_simple = request.get_json(force=True) 
  element_callback = fase_model.ElementCallback.FromSimple(element_callback_simple)
  response_simple, code = SafeCall(
      fase_server.FaseServer.Get().ElementCallback, element_callback, session_info, screen_info)
  response_simple = CleanSimple(response_simple)
  return jsonify(**response_simple), code


@application.route('/getresource/filename/<path:filename>', methods=['GET', 'OPTIONS'])
def getresource(filename):
  resource_dir = os.path.dirname(sys.modules[fase.Service.service_cls.__module__].__file__)
  filename = os.path.join(*filename.split('/'))
  return send_file(os.path.join(resource_dir, filename))
