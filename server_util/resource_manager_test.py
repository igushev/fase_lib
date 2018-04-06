import os
import tempfile
import unittest

import resource_manager


class ResourceUtilTest(unittest.TestCase):

  def setUp(self):
    self.dirpath = tempfile.mkdtemp()
    for filename in [
        'images_1_5',
        'images_3_0',
        'images_2_0',
        'images_5_0',
        'images_big']:
      open(os.path.join(self.dirpath, filename), 'w').close()
    resource_manager.ResourceManager.Set(resource_manager.ResourceManager(self.dirpath), overwrite=True)

  def testTemplate(self):
    for pixel_density, expected_filename in [(0.0, 'images_1_5'),
                                             (0.5, 'images_1_5'),
                                             (1.0, 'images_1_5'),
                                             (1.5, 'images_1_5'),
                                             (2.0, 'images_2_0'),
                                             (2.5, 'images_2_0'),
                                             (3.0, 'images_3_0'),
                                             (3.5, 'images_3_0'),
                                             (4.0, 'images_3_0'),
                                             (4.5, 'images_3_0'),
                                             (5.0, 'images_5_0'),
                                             (5.5, 'images_5_0'),
                                             (6.0, 'images_5_0')]:
      self.assertEqual(expected_filename,
                       resource_manager.ResourceManager.Get().GetResourceFilename('images_@', pixel_density))

  def testTemplateNoPixelDensity(self):
    self.assertEqual('images_1_5', resource_manager.ResourceManager.Get().GetResourceFilename('images_@', None))

  def testTemplateNotFound(self):
    self.assertIsNone(resource_manager.ResourceManager.Get().GetResourceFilename('image_@', 1.5))

  def testFilename(self):
    self.assertEqual('images_big', resource_manager.ResourceManager.Get().GetResourceFilename('images_big', 1.5))
      
  def testFilenameNotFound(self):
    self.assertIsNone(resource_manager.ResourceManager.Get().GetResourceFilename('images_small', 1.5))


if __name__ == '__main__':
    unittest.main()
