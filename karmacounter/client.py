import logging
import requests

from karmacounter import data as kc_data 

URL = 'http://karmacounter-env-test1.us-west-2.elasticbeanstalk.com/'


def AssertStatus(http_response):
  if http_response.status_code != requests.codes.ok:
    logging.error(http_response.text)
    http_response.raise_for_status()


# TODO(igushev): Add key to GetUserSession. 
def GetUserSession(new_user):
  url = URL + '/getusersession'
  new_user_simple = new_user.ToSimple()
  http_response = requests.post(url, json=new_user_simple)
  AssertStatus(http_response)
  session_info_simple = http_response.json()
  return kc_data.SessionInfo.FromSimple(session_info_simple)


def GetStartingPage(session_info):
  url = URL + '/getstartingpage'
  headers = {'session-id': session_info.session_id}
  http_response = requests.get(url, headers=headers)
  AssertStatus(http_response)
  starting_page_simple = http_response.json()
  return kc_data.StartingPage.FromSimple(starting_page_simple) 


def _SendObjectGetStatus(http_request_name, obj, session_info):
  url = URL + http_request_name
  headers = {'session-id': session_info.session_id}
  obj_simple = obj.ToSimple()
  http_response = requests.post(url, headers=headers, json=obj_simple)
  AssertStatus(http_response)
  status_simple = http_response.json()
  return kc_data.Status.FromSimple(status_simple)


def AddUserEvent(new_user_event, session_info):
  return _SendObjectGetStatus('/adduserevent', new_user_event, session_info)


def AddOtherUserEvent(new_other_user_event, session_info):
  return _SendObjectGetStatus('/addotheruserevent', new_other_user_event, session_info)


def _GetUserEvents(http_request_name, session_info):
  url = URL + http_request_name
  headers = {'session-id': session_info.session_id}
  http_response = requests.get(url, headers=headers)
  AssertStatus(http_response)
  user_events_simple = http_response.json()
  return kc_data.ExternalUserEvents.FromSimple(user_events_simple) 


def GetUserEvents(session_info):
  return _GetUserEvents('/getuserevents', session_info)


def GetOtherUserEvents(session_info):
  return _GetUserEvents('/getotheruserevents', session_info)


def GetRegisteredUsers(request_registered_users, session_info):
  url = URL + '/getregisteredusers'
  headers = {'session-id': session_info.session_id}
  request_registered_users_simple = request_registered_users.ToSimple()
  http_response = requests.post(url, headers=headers, json=request_registered_users_simple)
  AssertStatus(http_response)
  registered_users_simple = http_response.json()
  return kc_data.RegisteredUsers.FromSimple(registered_users_simple)


def CitiesStatisticsTopBottom(session_info):
  url = URL + '/citiesstatisticsstopbottom'
  headers = {'session-id': session_info.session_id}
  http_response = requests.get(url, headers=headers)
  AssertStatus(http_response)
  cities_statistics_top_bottom_simple = http_response.json()
  return kc_data.ExternalCitiesStatisticsTopBottom.FromSimple(cities_statistics_top_bottom_simple) 


def AcceptUserEvent(user_event_info, session_info):
  return _SendObjectGetStatus('/acceptuserevent', user_event_info, session_info)


def RejectUserEvent(user_event_info, session_info):
  return _SendObjectGetStatus('/rejectuserevent', user_event_info, session_info)


def DeleteUserEvent(user_event_info, session_info):
  return _SendObjectGetStatus('/deleteuserevent', user_event_info, session_info)


def ReportAbuse(user_event_info, session_info):
  return _SendObjectGetStatus('/reportabuse', user_event_info, session_info)


def ReportSpam(user_event_info, session_info):
  return _SendObjectGetStatus('/reportspam', user_event_info, session_info)


def BlockUser(user_event_info, session_info):
  return _SendObjectGetStatus('/blockuser', user_event_info, session_info)
