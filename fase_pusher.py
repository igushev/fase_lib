"""Fase Push Notifications."""


fase_pusher_impl = None


def Push(user_id, title, message):
  """Push notification to user by given Fase user id with given title and message."""
  return fase_pusher_impl.Push(user_id, title, message)
