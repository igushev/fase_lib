import copy
import datetime
import hashlib

from base_util import data_util
from base_util import datetime_util
import json_util


MIN_AGE_YEARS = 13


ADDED_BY = 'Added by %s'
WAITING_FOR = 'Waiting for action from %s'
ACTION_BY = '%s by %s'
ADDED_BY_NO_WITNESS = (
    'Added by %s without a witness. Not part of your city\'s statistics')
YOU = 'you'

class VerificationStatus(object):
  pending = 'PENDING'
  accepted = 'ACCEPTED'
  rejected = 'REJECTED'


@json_util.JSONDecorator({
    'command': json_util.JSONString()})
class Command(data_util.AbstractObject):

  def __init__(self, command):
    self.command = command


@json_util.JSONDecorator({
    'select_score_list': json_util.JSONList(json_util.JSONInt()),
    'show_cities_statistics': json_util.JSONBool(),
    'show_cup_of_coffee': json_util.JSONBool()})
class AppConfig(data_util.AbstractObject):
  
  def __init__(self, select_score_list, show_cities_statistics,
               show_cup_of_coffee):
    self.select_score_list = select_score_list
    self.show_cities_statistics = show_cities_statistics
    self.show_cup_of_coffee = show_cup_of_coffee


@json_util.JSONDecorator({
    'device_type': json_util.JSONString(),
    'device_token': json_util.JSONString()})
class Device(data_util.AbstractObject):

  def __init__(self, device_type, device_token):
    self.device_type = device_type
    self.device_token = device_token


@json_util.JSONDecorator({
    'country_code': json_util.JSONString()})
class Locale(data_util.AbstractObject):

  def __init__(self, country_code):
    self.country_code = country_code


@json_util.JSONDecorator({
    'google_place_id': json_util.JSONString(),
    'city': json_util.JSONString(),
    'state': json_util.JSONString(),
    'country': json_util.JSONString(),
    'city_id': json_util.JSONString()})
class CommonCity(data_util.AbstractObject):

  def __init__(self,
               google_place_id=None,
               city=None,
               state=None,
               country=None):
    self.google_place_id = google_place_id
    self.city = city
    self.state = state
    self.country = country
    self.ComputeCityId()

  def ComputeCityId(self):
    m = hashlib.md5()
    # TODO(igushev): Switch to codes.
    m.update((self.city or '').encode('utf-8'))
    m.update((self.state or '').encode('utf-8'))
    m.update((self.country or '').encode('utf-8'))
    self.city_id = m.hexdigest()

  def WithoutCityId(self):
    res = copy.copy(self)
    del res.city_id
    return res

  def ToCityStatistics(self):
    kwargs = copy.copy(self.__dict__)
    kwargs.pop('city_id')
    return CityStatistics(**kwargs)

  def Display(self):
    return ('%s, %s, %s' % (self.city, self.state, self.country)
            if self.state else
            '%s, %s' % (self.city, self.country))


@json_util.JSONDecorator({
    'phone_number': json_util.JSONString(),
    'first_name': json_util.JSONString(),
    'last_name': json_util.JSONString()})
class BasicUser(data_util.AbstractObject):

  def __init__(self,
               phone_number=None,
               first_name=None,
               last_name=None):
    self.phone_number = phone_number
    self.first_name = first_name
    self.last_name = last_name

  def Display(self):
    if self.first_name and self.last_name:
      return ' '.join([self.first_name, self.last_name])
    elif self.first_name:
      return self.first_name
    elif self.last_name:
      return self.last_name
    else:
      return self.phone_number


@json_util.JSONDecorator({
    'display_name': json_util.JSONString()})
class PublicUser(BasicUser):

  def __init__(self,
               display_name=None,
               **kwargs):
    super(PublicUser, self).__init__(**kwargs)
    self.display_name = display_name


# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'city': json_util.JSONObject(CommonCity),
    'date_of_birth': json_util.JSONDate()})
class CommonUser(BasicUser):

  def __init__(self,
               city=None,
               date_of_birth=None,
               **kwargs):
    super(CommonUser, self).__init__(**kwargs)
    self.city = city
    self.date_of_birth = date_of_birth


# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'device': json_util.JSONObject(Device),
    'locale': json_util.JSONObject(Locale),
    'code': json_util.JSONString()})
class NewUser(CommonUser):

  def __init__(self,
               device=None,
               locale=None,
               code=None,
               **kwargs):
    super(NewUser, self).__init__(**kwargs)
    self.device = device
    self.locale = locale
    self.code = code

  def ToUser(self):
    kwargs = copy.copy(self.__dict__)
    kwargs.pop('device')
    kwargs.pop('code')
    return User(**kwargs)


# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'user_id': json_util.JSONString(),
    'registered': json_util.JSONBool(),
    'score': json_util.JSONInt(),
    'locale': json_util.JSONObject(Locale),
    'inferred_country_code': json_util.JSONString(),
    'showed_info': json_util.JSONBool(),
    'datetime_added': json_util.JSONString()})
class User(CommonUser):

  def __init__(self,
               user_id=None,
               registered=None,
               score=None,
               locale=None,
               inferred_country_code=None,
               showed_info=None,
               datetime_added=None,
               **kwargs):
    super(User, self).__init__(**kwargs)
    self.user_id = user_id
    self.registered = registered
    self.score = score
    self.locale = locale
    self.inferred_country_code = inferred_country_code
    self.showed_info = showed_info
    self.datetime_added = datetime_added

  def ToPublicUser(self):
    kwargs = copy.copy(self.__dict__)
    kwargs.pop('user_id')
    kwargs.pop('registered')
    kwargs.pop('score')
    kwargs.pop('locale')
    kwargs.pop('inferred_country_code')
    kwargs.pop('showed_info')
    kwargs.pop('datetime_added')
    kwargs.pop('city')
    kwargs.pop('date_of_birth')
    kwargs['display_name'] = self.Display()
    return PublicUser(**kwargs)

  def ToExternalUser(self):
    kwargs = copy.copy(self.__dict__)
    kwargs['city'] = kwargs['city'].WithoutCityId()
    kwargs.pop('user_id')
    kwargs.pop('registered')
    kwargs.pop('locale')
    kwargs.pop('inferred_country_code')
    kwargs.pop('showed_info')
    kwargs.pop('datetime_added')
    kwargs['display_name'] = self.Display()
    return ExternalUser(**kwargs)


# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'display_name': json_util.JSONString(),
    'score': json_util.JSONInt()})
class ExternalUser(CommonUser):

  def __init__(self,
               display_name=None,
               score=None,
               **kwargs):
    super(ExternalUser, self).__init__(**kwargs)
    self.display_name = display_name
    self.score = score


@json_util.JSONDecorator({
    'phone_number': json_util.JSONString(),
    'device': json_util.JSONObject(Device),
    'locale': json_util.JSONObject(Locale)})
class UserCredentials(data_util.AbstractObject):
  
  def __init__(self, phone_number, device, locale):
    self.phone_number = phone_number
    self.device = device
    self.locale = locale


@json_util.JSONDecorator({
    'user_id': json_util.JSONString()})
class UserInfo(data_util.AbstractObject):
  
  def __init__(self, user_id):
    self.user_id = user_id


@json_util.JSONDecorator({
    'activation_code': json_util.JSONInt()})
class Activation(data_util.AbstractObject):
  
  def __init__(self, activation_code):
    self.activation_code = activation_code


@json_util.JSONDecorator({
    'session_id': json_util.JSONString(),
    'user_id': json_util.JSONString(),
    'device': json_util.JSONObject(Device),
    'activation_code': json_util.JSONInt(),
    'datetime_added': json_util.JSONString()})
class Session(data_util.AbstractObject):

  def __init__(self, session_id, user_id, device, activation_code,
               datetime_added):
    self.session_id = session_id
    self.user_id = user_id
    self.device = device
    self.activation_code = activation_code
    self.datetime_added = datetime_added

  def ToSessionInfo(self):
    return SessionInfo(self.session_id)


@json_util.JSONDecorator({
    'session_id': json_util.JSONString()})
class SessionInfo(data_util.AbstractObject):

  def __init__(self, session_id):
    self.session_id = session_id


# NOTE(igushev): UserEvent which is sent by frontend.
@json_util.JSONDecorator({
    'score': json_util.JSONInt(),
    'description': json_util.JSONString(),
    'witness_phone_number': json_util.JSONString(),
    'witness_display_name': json_util.JSONString(),
    'invite_witness': json_util.JSONBool(),
    'cup_of_coffee': json_util.JSONBool()})
class NewUserEvent(data_util.AbstractObject):

  def __init__(self, score, description, witness_phone_number=None,
               witness_display_name=None, invite_witness=False,
               cup_of_coffee=False):
    self.score = score
    self.description = description
    self.witness_phone_number = witness_phone_number
    self.witness_display_name = witness_display_name
    self.invite_witness = invite_witness
    self.cup_of_coffee = cup_of_coffee


# NOTE(igushev): UserEvent which is sent by frontend for another user.
@json_util.JSONDecorator({
    'phone_number': json_util.JSONString(),
    'score': json_util.JSONInt(),
    'description': json_util.JSONString(),
    'other_user_display_name': json_util.JSONString(),
    'invite_other_user': json_util.JSONBool(),
    'cup_of_coffee': json_util.JSONBool()})
class NewOtherUserEvent(data_util.AbstractObject):

  def __init__(self, phone_number, score, description,
               other_user_display_name=None, invite_other_user=False,
               cup_of_coffee=False):
    self.phone_number = phone_number
    self.score = score
    self.description = description
    self.other_user_display_name = other_user_display_name
    self.invite_other_user = invite_other_user
    self.cup_of_coffee = cup_of_coffee


# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'event_id': json_util.JSONString(),
    'datetime': json_util.JSONDateTime(),
    'user': json_util.JSONObject(PublicUser),
    'score': json_util.JSONInt(),
    'description': json_util.JSONString(),
    'witness': json_util.JSONObject(PublicUser),
    'verification_status': json_util.JSONString()})
class CommonUserEvent(data_util.AbstractObject):
  
  def __init__(self,
               event_id=None,
               datetime=None,
               user=None,
               score=None,
               description=None,
               witness=None,
               verification_status=None):
    self.event_id = event_id
    self.datetime = datetime
    self.user = user
    self.score = score
    self.description = description
    self.witness = witness
    self.verification_status = verification_status


# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'user_id': json_util.JSONString(),
    'initiator_user_id': json_util.JSONString(),
    'witness_user_id': json_util.JSONString(),
    'datetime_added': json_util.JSONString()})
class UserEvent(CommonUserEvent):
  
  def __init__(self,
               user_id=None,
               initiator_user_id=None,
               witness_user_id=None,
               datetime_added=None,
               **kwargs):
    super(UserEvent, self).__init__(**kwargs)
    self.user_id = user_id
    self.initiator_user_id = initiator_user_id
    self.witness_user_id = witness_user_id
    self.datetime_added = datetime_added

  def DisplayStatus(self, receiver_user_id):
    def DisplayUser(receiver_user_id, user_id, user):
      if receiver_user_id == user_id:
        return YOU
      else:
        return user.display_name

    display_status_list = []
    self_added = self.user_id == self.initiator_user_id
    if self.witness_user_id:
      initiator_user = self.user if self_added else self.witness
      action_user_id = self.witness_user_id if self_added else self.user_id
      action_user = self.witness if self_added else self.user
      display_status_list.append(
          ADDED_BY %
          DisplayUser(receiver_user_id, self.initiator_user_id, initiator_user))
      if self.verification_status == VerificationStatus.pending:
        display_status_list.append(
            WAITING_FOR %
            DisplayUser(receiver_user_id, action_user_id, action_user))
      else:
        display_status_list.append(
            ACTION_BY %
            (self.verification_status.title(),
             DisplayUser(receiver_user_id, action_user_id, action_user)))
    else:
      assert self_added
      assert receiver_user_id == self.user_id
      display_status_list.append(ADDED_BY_NO_WITNESS % YOU)
    return '. '.join(display_status_list)

  def ToExternalUserEvent(self, receiver_user_id):
    kwargs = copy.copy(self.__dict__)
    kwargs.pop('user_id')
    kwargs.pop('initiator_user_id')
    kwargs.pop('witness_user_id')
    kwargs.pop('datetime_added')
    kwargs['self_added'] = (self.user_id == self.initiator_user_id)
    kwargs['display_status'] = self.DisplayStatus(receiver_user_id)
    kwargs['display_datetime'] = (
        datetime_util.GetDatetimeDiffStr(self.datetime, datetime.datetime.now()))
    
    return ExternalUserEvent(**kwargs)
    

# TODO(igushev): Clean up None.
@json_util.JSONDecorator({
    'self_added': json_util.JSONBool(),
    'display_status': json_util.JSONString(),
    'display_datetime': json_util.JSONString()})
class ExternalUserEvent(CommonUserEvent):
  
  def __init__(self,
               self_added=None,
               display_status=None,
               display_datetime=None,
               **kwargs):
    super(ExternalUserEvent, self).__init__(**kwargs)
    self.self_added = self_added
    self.display_status = display_status
    self.display_datetime = display_datetime

@json_util.JSONDecorator({
    'event_id': json_util.JSONString()})
class UserEventInfo(data_util.AbstractObject):

  def __init__(self, event_id):
    self.event_id = event_id


@json_util.JSONDecorator({
    'events': json_util.JSONList(json_util.JSONObject(ExternalUserEvent))})
class ExternalUserEvents(data_util.AbstractObject):

  def __init__(self, events):
    self.events = events

  def __str__(self):
    return '\n'.join(['User Events:'] +
                     [str(event) for event in self.events])


@json_util.JSONDecorator({
    'user': json_util.JSONObject(ExternalUser),
    'events_count': json_util.JSONInt(),
    'events': json_util.JSONList(json_util.JSONObject(ExternalUserEvent)),
    'other_events_count': json_util.JSONInt(),
    'other_events':
    json_util.JSONList(json_util.JSONObject(ExternalUserEvent)),
    'app_config': json_util.JSONObject(AppConfig),
    'info': json_util.JSONString()})
class StartingPage(data_util.AbstractObject):

  def __init__(self, user, events_count, events, other_events_count,
               other_events, app_config, info):
    self.user = user
    self.events_count = events_count
    self.events = events
    self.other_events_count = other_events_count
    self.other_events = other_events
    self.app_config = app_config
    self.info = info

  def __str__(self):
    return '\n'.join(['User: %s' % self.user,
                      'User Events Count: %d' % self.events_count,
                      'User Events:'] +
                     [str(event) for event in self.events] +
                     ['Other User Events Count: %d' % self.other_events_count,
                      'Other User Events:'] +
                     [str(event) for event in self.other_events] +
                     ['App Config: %s' % self.app_config] +
                     ['Info: %s' % self.info])


@json_util.JSONDecorator({
    'phone_number_list': json_util.JSONList(json_util.JSONString())})
class RequestRegisteredUsers(data_util.AbstractObject):

  def __init__(self, phone_number_list=None):
    self.phone_number_list = phone_number_list or []


@json_util.JSONDecorator({
    'users': json_util.JSONList(json_util.JSONObject(PublicUser))})
class RegisteredUsers(data_util.AbstractObject):

  def __init__(self, users):
    self.users = users

  def __str__(self):
    return '\n'.join(['User: %s' % user for user in self.users])

@json_util.JSONDecorator({
    'total_score': json_util.JSONInt(),
    'total_count': json_util.JSONInt(),
    'average_score_fake_id': json_util.JSONString(),
    'average_score': json_util.JSONFloat()})
class CityStatistics(CommonCity):

  def __init__(self,
               total_score=None,
               total_count=None,
               average_score_fake_id=None,
               average_score=None,
               **kwargs):
    super(CityStatistics, self).__init__(**kwargs)
    self.total_score = total_score
    self.total_count = total_count
    self.average_score_fake_id = average_score_fake_id
    self.average_score = average_score

  def ToExternalCityStatistics(self):
    kwargs = copy.copy(self.__dict__)
    kwargs.pop('city_id')
    kwargs.pop('total_score')
    kwargs.pop('total_count')
    kwargs.pop('average_score_fake_id')
    kwargs.pop('average_score')
    kwargs['display_name'] = self.Display()
    kwargs['display_score'] = '%.2f' % self.average_score
    return ExternalCityStatistics(**kwargs)


@json_util.JSONDecorator({
    'city': json_util.JSONObject(CommonCity)})
class RequestCityStatistics(data_util.AbstractObject):

  def __init__(self, city):
    assert isinstance(city, CommonCity)
    self.city=city


@json_util.JSONDecorator({
    'display_name': json_util.JSONString(),
    'display_score': json_util.JSONString()})
class ExternalCityStatistics(CommonCity):

  def __init__(self, display_name=None, display_score=None, **kwargs):
    super(ExternalCityStatistics, self).__init__(**kwargs)
    self.display_name = display_name
    self.display_score = display_score


@json_util.JSONDecorator({
  'external_user': json_util.JSONObject(ExternalUser),
  'external_cities_statistics_top':
  json_util.JSONList(json_util.JSONObject(ExternalCityStatistics)),
  'external_cities_statistics_bottom':
  json_util.JSONList(json_util.JSONObject(ExternalCityStatistics))})
class ExternalCitiesStatisticsTopBottom(data_util.AbstractObject):

  def __init__(self,
               external_user,
               external_cities_statistics_top,
               external_cities_statistics_bottom):
    self.external_user = external_user
    self.external_cities_statistics_top = external_cities_statistics_top
    self.external_cities_statistics_bottom = external_cities_statistics_bottom

  def __str__(self):
    return '\n'.join(['User: %s' % self.external_user,
                      'Cities Top:'] +
                     [str(external_city_statistics)
                      for external_city_statistics
                      in self.external_cities_statistics_top] +
                     ['Cities Bottom:'] +
                     [str(external_city_statistics)
                      for external_city_statistics
                      in self.external_cities_statistics_bottom])


@json_util.JSONDecorator({
    'message': json_util.JSONString()})
class Status(data_util.AbstractObject):

  def __init__(self, message):
    self.message = message


@json_util.JSONDecorator({
    'code': json_util.JSONInt(),
    'message': json_util.JSONString()})
class BadRequest(data_util.AbstractObject):

  def __init__(self, code, message):
    self.code = code
    self.message = message
