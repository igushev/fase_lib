import functools
import os

TEMPLATE_SYMBOL = '@'
PIXEL_DENSITY_STEP = 0.25
PIXEL_DENSITY_MIN = 0
PIXEL_DENSITY_MAX = 10


@functools.lru_cache(maxsize=None, typed=True)
def GetResourceFilename(resource_dir, filename, pixel_density):
  pixel_density = pixel_density or 1.0
  if TEMPLATE_SYMBOL in filename:
    return ResolveResourceFilename(resource_dir, filename, pixel_density)
  if os.path.isfile(os.path.join(resource_dir, filename)):
    return filename
  return None


def ResolveResourceFilename(resource_dir, filename_template, pixel_density):
  assert pixel_density % PIXEL_DENSITY_STEP == 0
  for direction in [-1, 1]:
    current_pixel_density = pixel_density
    while ((direction == -1 and current_pixel_density > PIXEL_DENSITY_MIN) or
           (direction == 1 and current_pixel_density < PIXEL_DENSITY_MAX)):
      current_pixel_density_str = ('%.1f' % current_pixel_density).replace('.', '_')
      filename = filename_template.replace(TEMPLATE_SYMBOL, current_pixel_density_str)
      if os.path.isfile(os.path.join(resource_dir, filename)):
        return filename
      current_pixel_density += PIXEL_DENSITY_STEP * direction
  return None
