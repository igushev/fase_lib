import os


class FaseResourceManager():

  def __init__(self, resource_dir, http_client):
    self.resource_dir = resource_dir
    self.http_client = http_client

  def PreloadResources(self, resources):
    get_resource_filename_list = []
    for resource in resources.resource_list:
      assert resource.filename is not None
      if not self.HasResourceFilename(resource.filename):
        get_resource_filename_list.append(resource.filename)

    for filename in get_resource_filename_list:
      self.http_client.GetResourceFilename(self.resource_dir, filename)

  def HasResourceFilename(self, filename):
    return os.path.isfile(os.path.join(self.resource_dir, filename))

  def GetResourceFilename(self, filename):
    return os.path.join(self.resource_dir, filename)
