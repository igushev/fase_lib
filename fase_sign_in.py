"""Fase Account Management."""


fase_sign_in_impl = None


def StartSignIn(service, on_done=None, on_skip=None, on_cancel=None, request_user_data=None):
  """Sign In user.

  Args:
    service: (Service)
    on_done: (Element.method) Call when user signed in.
    on_skip: (Element.method) Call when user decided to skip signing in.
    on_cancel: (Element.method) Call when user canceled signing in.
    request_user_data: (RequestUserData) Which data to request from user (Date of Birth, City, etc.)

  """
  return fase_sign_in_impl.StartSignIn(
      service, on_done=on_done, on_skip=on_skip, on_cancel=on_cancel, request_user_data=request_user_data)


def StartSignOut(service, on_cancel=None):
  """Sign Out user."""
  return fase_sign_in_impl.StartSignOut(service, on_cancel=on_cancel)


def GetUserIdByPhoneNumber(phone_number):
  """Get Fase user id by phone number."""
  return fase_sign_in_impl.GetUserIdByPhoneNumber(phone_number)
