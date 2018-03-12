import phonenumbers


class NoCountryCodeException(Exception):
  pass


class InvalidPhoneNumberException(Exception):
  pass


def _GetPhoneNumberObj(phone_number, country_code):
  try: 
    phone_number_obj = phonenumbers.parse(phone_number, country_code)
  except phonenumbers.phonenumberutil.NumberParseException:
    raise NoCountryCodeException()
  if not phonenumbers.is_possible_number(phone_number_obj):
    raise InvalidPhoneNumberException()
  return phone_number_obj


def Format(phone_number, country_code):
  phone_number_obj = _GetPhoneNumberObj(phone_number, country_code)
  return str(phonenumbers.format_number(
      phone_number_obj, phonenumbers.PhoneNumberFormat.E164))


def GetCountryCode(phone_number, country_code):
  phone_number_obj = _GetPhoneNumberObj(phone_number, country_code)
  return phonenumbers.region_code_for_number(phone_number_obj).upper()
