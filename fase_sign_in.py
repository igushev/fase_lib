fase_sign_in_impl = None


def StartSignIn(service, on_done=None, on_skip=None, on_cancel=None, request_user_data=None):
  return fase_sign_in_impl.StartSignIn(
      service, on_done=on_done, on_skip=on_skip, on_cancel=on_cancel, request_user_data=request_user_data)


def StartSignOut(service, on_cancel=None):
  return fase_sign_in_impl.StartSignOut(service, on_cancel=on_cancel)
