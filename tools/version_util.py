import os

FIRST_VERSION = '1.00.00.00'


def ReadVersion(version_filename):
  if os.path.exists(version_filename):
    return open(version_filename).readlines()[0]
  else:
    return FIRST_VERSION


def ReadAndUpdateVersion(version_filename, update_position=None):
  """Takes given filename containing version, optionally updates the version and saves it, and returns the version."""
  if os.path.exists(version_filename):
    current_version = open(version_filename).readlines()[0]
    numbers = current_version.split('.')
    if update_position:
      numbers[update_position] = '%02d' % (int(numbers[update_position]) + 1)
      if update_position < -1:
        numbers[update_position + 1:] = ['00'] * -(update_position + 1)
    version = '.'.join(numbers)
  else:
    version = FIRST_VERSION
  with open(version_filename, 'w') as fout:
    fout.write(version)
  print('\n'.join(['Version %s' % version]))
  return version
