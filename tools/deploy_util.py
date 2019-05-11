import os
import shutil
import tempfile


def Clean(dir_):
  os.system('find %s -name "__pycache__" | xargs rm -R' % dir_)


def Deploy(base_dir, copy_list, deploy_dir, deploy_filename):
  """Prepares archive of an application to be deployed in the cloud.
  
  Args:
    base_dir: (str) Directory of the application to be depoyed.
    copy_list: (list(tuple(str, str))) List of tuples of source and destination of files and directories to be copied
        into the archive. Source must be absolute path while destination must be relative to application directory.
        This does not affect input base_dir.
    deploy_dir: (str) Directory to put archive into.
    deploy_filename: (str) Filename without extension of output archive.
  """
  build_dir = os.path.join(tempfile.mkdtemp(), 'application')
  shutil.copytree(base_dir, build_dir)
  for src_path, dest_name in copy_list:
    shutil.copytree(src_path, os.path.join(build_dir, dest_name))

  Clean(build_dir)

  zip_dir = tempfile.mkdtemp()
  filepath = os.path.join(zip_dir, deploy_filename)
  zip_filepath = '%s.zip' % filepath 
  shutil.make_archive(filepath, 'zip', build_dir)
  shutil.rmtree(build_dir)

  final_filepath = os.path.join(deploy_dir, deploy_filename)
  final_zip_filepath = '%s.zip' % final_filepath
  os.makedirs(deploy_dir, exist_ok=True)
  if os.path.exists(final_zip_filepath):
    os.remove(zip_filepath)
    raise AssertionError('File %s already exisits' % final_zip_filepath)
  shutil.move(zip_filepath, final_zip_filepath)
  print('\n'.join(['Release name:', deploy_filename, 'Deploy file:', final_zip_filepath]))
