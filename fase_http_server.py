from flask import Flask, request, jsonify

import fase_model
import fase_server

application = Flask(__name__)
application.secret_key = 'fase_flask_secret_key'


@application.route('/sendinternalcommand', methods=['POST', 'OPTIONS'])
def sendinternalcommand():
  command_simple = request.get_json(force=True) 
  command = fase_model.Command.FromSimple(command_simple)
  status, code = fase_server.FaseServer.Get().SendInternalCommandSafe(command)
  status_simple = status.ToSimple()
  return jsonify(**status_simple), code


@application.route('/sendservicecommand', methods=['POST', 'OPTIONS'])
def sendservicecommand():
  command_simple = request.get_json(force=True) 
  command = fase_model.Command.FromSimple(command_simple)
  status, code = fase_server.FaseServer.Get().SendServiceCommandSafe(command)
  status_simple = status.ToSimple()
  return jsonify(**status_simple), code


@application.route('/getservice', methods=['POST', 'OPTIONS'])
def getservice():
  device_simple = request.get_json(force=True) 
  device = fase_model.Device.FromSimple(device_simple)
  response, code = fase_server.FaseServer.Get().GetServiceSafe(device)
  response_simple = response.ToSimple()
  return jsonify(**response_simple), code


@application.route('/getscreen', methods=['POST', 'OPTIONS'])
def getscreen():
  session_info = fase_model.SessionInfo(session_id=request.headers.get('session_id', None))
  response, code = fase_server.FaseServer.Get().GetScreenSafe(session_info)
  response_simple = response.ToSimple()
  return jsonify(**response_simple), code


@application.route('/screenupdate', methods=['POST', 'OPTIONS'])
def screenupdate():
  session_info = fase_model.SessionInfo(session_id=request.headers.get('session_id', None))
  screen_info = fase_model.ScreenInfo(screen_id=request.headers.get('screen_id', None))
  screen_update_simple = request.get_json(force=True) 
  screen_update = fase_model.ScreenUpdate.FromSimple(screen_update_simple)
  response, code = fase_server.FaseServer.Get().ScreenUpdateSafe(screen_update, session_info, screen_info)
  response_simple = response.ToSimple()
  return jsonify(**response_simple), code


@application.route('/elementclicked', methods=['POST', 'OPTIONS'])
def elementclicked():
  session_info = fase_model.SessionInfo(session_id=request.headers.get('session_id', None))
  screen_info = fase_model.ScreenInfo(screen_id=request.headers.get('screen_id', None))
  element_clicked_simple = request.get_json(force=True) 
  element_clicked = fase_model.ElementClicked.FromSimple(element_clicked_simple)
  response, code = fase_server.FaseServer.Get().ElementClickedSafe(element_clicked, session_info, screen_info)
  response_simple = response.ToSimple()
  return jsonify(**response_simple), code
