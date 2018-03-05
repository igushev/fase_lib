import os
import tempfile
import unittest

from fase_model import fase_model
import fase_resource_manager


class MockFaseHTTPClient(object):
  
  def __init__(self, resource_dir):
    self.resource_dir = resource_dir
    self.get_resource_filename_calls = 0

  def GetResourceFilename(self, resource_dir, filename):
    open(os.path.join(self.resource_dir, filename), 'w').close()
    self.get_resource_filename_calls += 1


class FaseResourceManagerTest(unittest.TestCase):

  def testGeneral(self):
    resource_dir = tempfile.mkdtemp()
    http_client = MockFaseHTTPClient(resource_dir)

    resource_manager = fase_resource_manager.FaseResourceManager(resource_dir, http_client)
    self.assertFalse(resource_manager.HasResourceFilename('a'))
    self.assertFalse(resource_manager.HasResourceFilename('b'))
    self.assertFalse(resource_manager.HasResourceFilename('c'))
    self.assertFalse(resource_manager.HasResourceFilename('d'))

    resource_list = [fase_model.Resource(filename='a'), fase_model.Resource(filename='b')]
    resources = fase_model.Resources(resource_list=resource_list)
    resource_manager.PreloadResources(resources)
    self.assertEqual(2, http_client.get_resource_filename_calls)
    self.assertTrue(resource_manager.HasResourceFilename('a'))
    self.assertTrue(resource_manager.HasResourceFilename('b'))
    self.assertFalse(resource_manager.HasResourceFilename('c'))
    self.assertFalse(resource_manager.HasResourceFilename('d'))

    resource_list = [fase_model.Resource(filename='a'), fase_model.Resource(filename='b'),
                     fase_model.Resource(filename='c'), fase_model.Resource(filename='d')]
    resources = fase_model.Resources(resource_list=resource_list)
    resource_manager.PreloadResources(resources)
    self.assertEqual(4, http_client.get_resource_filename_calls)
    self.assertTrue(resource_manager.HasResourceFilename('a'))
    self.assertTrue(resource_manager.HasResourceFilename('b'))
    self.assertTrue(resource_manager.HasResourceFilename('c'))
    self.assertTrue(resource_manager.HasResourceFilename('d'))

    resource_list = [fase_model.Resource(filename='b'), fase_model.Resource(filename='c')]
    resources = fase_model.Resources(resource_list=resource_list)
    resource_manager.PreloadResources(resources)
    self.assertEqual(4, http_client.get_resource_filename_calls)
    self.assertTrue(resource_manager.HasResourceFilename('a'))
    self.assertTrue(resource_manager.HasResourceFilename('b'))
    self.assertTrue(resource_manager.HasResourceFilename('c'))
    self.assertTrue(resource_manager.HasResourceFilename('d'))


if __name__ == '__main__':
    unittest.main()
