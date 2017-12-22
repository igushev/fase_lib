import os


def ReadAndUpdateVersion(version_filename, update_position=None):
  if os.path.exists(version_filename):
    current_version = open(version_filename).readlines()[0]
    numbers = current_version.split('.')
    if update_position:
      numbers[update_position] = '%02d' % (int(numbers[update_position]) + 1)
      if update_position < -1:
        numbers[update_position + 1:] = ['00'] * -(update_position + 1)
    version = '.'.join(numbers)
  else:
    version = '1.00.00.00'
  with open(version_filename, 'w') as fout:
    fout.write(version)
  print('\n'.join(['Version %s' % version]))
  return version


def Clean():
  os.system('find . -name "*.pyc" | xargs rm')
  os.system('find . -name "*~" | xargs rm')


def Deploy(deploy_dir, filename):
  os.system('mkdir -p %s' % deploy_dir)
  zip_filename = '%s.zip' % filename
  zip_final_filepath = os.path.join(deploy_dir, zip_filename)
  os.system('zip -r %s .' % zip_filename)
  if os.path.exists(zip_final_filepath):
    os.remove(zip_filename)
    raise AssertionError('File %s already exisits' % zip_final_filepath)
  os.system('mv %s %s' % (zip_filename, zip_final_filepath))
  print('\n'.join(['Release name:',
                   filename,
                   'Deploy file:',
                   zip_final_filepath]))
