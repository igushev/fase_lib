import logging
import requests

from base_util import singleton_util

from karmacounter_fase import data as kc_data 


@singleton_util.Singleton()
class KarmaCounterClient(object):

  def __init__(self, server_url):
    self.server_url = server_url

  @staticmethod
  def AssertStatus(http_response):
    if http_response.status_code != requests.codes.ok:
      logging.error(http_response.text)
      http_response.raise_for_status()
  
  def GetUserSession(self, new_user):
    url = self.server_url + '/getusersession'
    new_user_simple = new_user.ToSimple()
    http_response = requests.post(url, json=new_user_simple)
    KarmaCounterClient.AssertStatus(http_response)
    session_info_simple = http_response.json()
    return kc_data.SessionInfo.FromSimple(session_info_simple)
  
  def GetStartingPage(self, session_info):
    url = self.server_url + '/getstartingpage'
    headers = {'session-id': session_info.session_id}
    http_response = requests.get(url, headers=headers)
    KarmaCounterClient.AssertStatus(http_response)
    starting_page_simple = http_response.json()
    return kc_data.StartingPage.FromSimple(starting_page_simple) 
  
  def _SendObjectSessionGetStatus(self, http_request_name, obj, session_info):
    url = self.server_url + http_request_name
    headers = {'session-id': session_info.session_id}
    obj_simple = obj.ToSimple()
    http_response = requests.post(url, headers=headers, json=obj_simple)
    KarmaCounterClient.AssertStatus(http_response)
    status_simple = http_response.json()
    return kc_data.Status.FromSimple(status_simple)
  
  def AddUserEvent(self, new_user_event, session_info):
    return self._SendObjectSessionGetStatus('/adduserevent', new_user_event, session_info)
  
  def AddOtherUserEvent(self, new_other_user_event, session_info):
    return self._SendObjectSessionGetStatus('/addotheruserevent', new_other_user_event, session_info)
  
  def _GetUserEvents(self, http_request_name, session_info):
    url = self.server_url + http_request_name
    headers = {'session-id': session_info.session_id}
    http_response = requests.get(url, headers=headers)
    KarmaCounterClient.AssertStatus(http_response)
    user_events_simple = http_response.json()
    return kc_data.ExternalUserEvents.FromSimple(user_events_simple) 
  
  def GetUserEvents(self, session_info):
    return self._GetUserEvents('/getuserevents', session_info)
  
  def GetOtherUserEvents(self, session_info):
    return self._GetUserEvents('/getotheruserevents', session_info)
  
  def GetRegisteredUsers(self, request_registered_users, session_info):
    url = self.server_url + '/getregisteredusers'
    headers = {'session-id': session_info.session_id}
    request_registered_users_simple = request_registered_users.ToSimple()
    http_response = requests.post(url, headers=headers, json=request_registered_users_simple)
    KarmaCounterClient.AssertStatus(http_response)
    registered_users_simple = http_response.json()
    return kc_data.RegisteredUsers.FromSimple(registered_users_simple)
  
  def CitiesStatisticsTopBottom(self, session_info):
    url = self.server_url + '/citiesstatisticsstopbottom'
    headers = {'session-id': session_info.session_id}
    http_response = requests.get(url, headers=headers)
    KarmaCounterClient.AssertStatus(http_response)
    cities_statistics_top_bottom_simple = http_response.json()
    return kc_data.ExternalCitiesStatisticsTopBottom.FromSimple(cities_statistics_top_bottom_simple) 
  
  def AcceptUserEvent(self, user_event_info, session_info):
    return self._SendObjectSessionGetStatus('/acceptuserevent', user_event_info, session_info)
  
  def RejectUserEvent(self, user_event_info, session_info):
    return self._SendObjectSessionGetStatus('/rejectuserevent', user_event_info, session_info)
  
  def DeleteUserEvent(self, user_event_info, session_info):
    return self._SendObjectSessionGetStatus('/deleteuserevent', user_event_info, session_info)
  
  def ReportAbuse(self, user_event_info, session_info):
    return self._SendObjectSessionGetStatus('/reportabuse', user_event_info, session_info)
  
  def ReportSpam(self, user_event_info, session_info):
    return self._SendObjectSessionGetStatus('/reportspam', user_event_info, session_info)
  
  def BlockUser(self, user_event_info, session_info):
    return self._SendObjectSessionGetStatus('/blockuser', user_event_info, session_info)
