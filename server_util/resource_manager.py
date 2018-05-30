import functools
import os

from base_util import singleton_util

TEMPLATE_SYMBOL = '@'
PIXEL_DENSITY_STEP = 0.25
PIXEL_DENSITY_MIN = 0
PIXEL_DENSITY_MAX = 10


@singleton_util.Singleton()
class ResourceManager():

  def __init__(self, resource_dir):
    self.resource_dir = resource_dir

  def GetResourceDir(self):
    return self.resource_dir

  @functools.lru_cache(maxsize=None, typed=True)
  def GetResourceFilename(self, filename, pixel_density):
    if TEMPLATE_SYMBOL in filename:
      return self.ResolveResourceFilename(filename, pixel_density)
    if os.path.isfile(os.path.join(self.resource_dir, filename)):
      return filename
    return None
  
  def ResolveResourceFilename(self, filename_template, pixel_density):
    assert pixel_density % PIXEL_DENSITY_STEP == 0
    for direction in [-1, 1]:
      current_pixel_density = pixel_density
      while ((direction == -1 and current_pixel_density > PIXEL_DENSITY_MIN) or
             (direction == 1 and current_pixel_density < PIXEL_DENSITY_MAX)):
        current_pixel_density_str = ('%.2f' % current_pixel_density).replace('.', '_')
        filename = filename_template.replace(TEMPLATE_SYMBOL, current_pixel_density_str)
        if os.path.isfile(os.path.join(self.resource_dir, filename)):
          return filename
        current_pixel_density += PIXEL_DENSITY_STEP * direction
    return None
