import os
import shutil
import tempfile


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


def Clean(dir_):
  os.system('find %s -name "__pycache__" | xargs rm -R' % dir_)


def Deploy(home_dir, dep_list, move_list, deploy_dir, filename):
  build_dir = tempfile.mkdtemp()
  for dep in dep_list:
    shutil.copytree(os.path.join(home_dir, dep), os.path.join(build_dir, dep))
  for move_from, move_to in move_list:
    shutil.move(os.path.join(build_dir, move_from), os.path.join(build_dir, move_to))

  Clean(build_dir)

  zip_dir = tempfile.mkdtemp()
  filepath = os.path.join(zip_dir, filename)
  zip_filepath = '%s.zip' % filepath 
  shutil.make_archive(filepath, 'zip', build_dir)
  shutil.rmtree(build_dir)

  final_filepath = os.path.join(deploy_dir, filename)
  final_zip_filepath = '%s.zip' % final_filepath
  os.makedirs(deploy_dir, exist_ok=True)
  if os.path.exists(final_zip_filepath):
    os.remove(zip_filepath)
    raise AssertionError('File %s already exisits' % final_zip_filepath)
  shutil.move(zip_filepath, final_zip_filepath)
  print('\n'.join(['Release name:', filename, 'Deploy file:', final_zip_filepath]))
