from collections import namedtuple

from fase import fase
from fase_client import fase_ui

MIN = 1
MAX = 2

SCREEN_HEGHT = 1200
SCREEN_WIDTH = 800

VERTICAL = 1
HORIZONAL = 2

class Sizes(object):
  
  def __init__(self, height, width):
    self.height = height
    self.width = width

  def __repr__(self):
    return '%d x %d' % (self.height, self.width)


def MaxElement(element, outer_orientation):
  # Only element which has field size and it equal to MAX
  if hasattr(element, 'size') and element.size == MAX:
    # Consider Frame which has size MAX only if it has same orientation.
    if ((isinstance(element, fase.Frame) and element.orientation == outer_orientation) or
        not isinstance(element, fase.Frame)):
      return True
  return False


def AddSizes(sizes_to, sizes_add, orientation):
  if orientation == VERTICAL:
    return Sizes(sizes_to.height + sizes_add.height, max(sizes_to.width, sizes_add.width))
  else:
    return Sizes(max(sizes_to.height, sizes_add.height), (sizes_to.width + sizes_add.width))


def SubstractSizes(sizes_from, sizes_sub, orientation):
  if orientation == VERTICAL:
    return Sizes(sizes_from.height - sizes_sub.height, sizes_from.width)
  else:
    return Sizes(sizes_from.height, sizes_from.width - sizes_sub.width)


def DistributedSizes(sizes_dist, num, orientation):
  if orientation == VERTICAL:
    return Sizes(sizes_dist.height / num, sizes_dist.width)
  else:
    return Sizes(sizes_dist.height, sizes_dist.width / num)


def AssertFit(size, size_fit):
  assert size_fit.height <= size.height, (size, size_fit)
  assert size_fit.width <= size.width, (size, size_fit)


def DrawElement(id_list, element, outer_orientation, outer_sizes):
  if isinstance(element, fase.Frame):
    element_sizes = DrawFrameElement(id_list, element, element.orientation, outer_sizes)
  else:
    # Create a platform specific object.
    ui_element = object()
    element_sizes = Sizes(200, 300)
  # If it has size MAX, stretch along outer_orientation
  if MaxElement(element, outer_orientation):
    if outer_orientation == VERTICAL:
      element_sizes.height = outer_sizes.height
    else:
      element_sizes.width = outer_sizes.width
  # Take care of alignment here.
  return element_sizes


def DrawFrameElement(frame_id_list, frame_element, frame_orientation, frame_sizes, scroll_frame=False):
  num_max_elements = 0
  sum_element_sizes = Sizes(0, 0)
  for id_, element in frame_element.GetIdElementList():
    # Skip built in element like navigation bar, main menus, etc.
    if id_ in fase_ui.BUILT_IN_IDS:
      continue
    # Skip elements which have size MAX.
    if MaxElement(element, frame_orientation):
      num_max_elements += 1
      continue
    # Draw actual element and get it actual sizes.
    id_list = frame_id_list + [id_]
    element_size = DrawElement(id_list, element, frame_orientation, frame_sizes)
    sum_element_sizes = AddSizes(sum_element_sizes, element_size, frame_orientation)

  if not scroll_frame:
    AssertFit(frame_sizes, sum_element_sizes)
  if not num_max_elements:
    return sum_element_sizes

  assert not scroll_frame
  # Distribute the rest of the screen among elements with size MAX
  sizes_left = SubstractSizes(frame_sizes, sum_element_sizes, frame_orientation)
  max_element_sizes = DistributedSizes(sizes_left, num_max_elements, frame_orientation)

  for id_, element in frame_element.GetIdElementList():
    # Skip built in element like navigation bar, main menus, etc.
    if id_ in fase_ui.BUILT_IN_IDS:
      continue
    # Draw elements which have size MAX.
    if MaxElement(element, frame_orientation):
      # Draw actual element and get it actual sizes.
      id_list = frame_id_list + [id_]
      element_size = DrawElement(id_list, element, frame_orientation, max_element_sizes)
      sum_element_sizes = AddSizes(sum_element_sizes, element_size, frame_orientation)
  return sum_element_sizes

  
def DrawScreen(screen):
  screen_sizes = Sizes(SCREEN_HEGHT, SCREEN_WIDTH)
  DrawFrameElement([], screen, VERTICAL, screen_sizes, scroll_frame=screen.scrollable)
