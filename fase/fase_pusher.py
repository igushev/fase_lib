fase_pusher_impl = None


def Push(user_id, title, message):
  return fase_pusher_impl.Push(user_id, title, message)
