import re

DEMO_PHONE_REGEXP = '\+100000000[0-9][0-9]'
DEMO_ACTIVATION_CODE = 321654


def PhoneNumberIsDemo(phone_number):
  return re.fullmatch(DEMO_PHONE_REGEXP, phone_number) is not None
