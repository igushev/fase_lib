import fase


class FaseUI(object):

  def __init__(self, ui_imp):
    self.ui_imp = ui_imp
    self.ui_imp.SetUI(self)
    self.id_list_to_value = dict()

  def SetClient(self, client):
    self.client = client

  def ResetValues(self):
    self.id_list_to_value = dict()

  def DrawScreen(self, screen):
    ui_imp_window = self.ui_imp.ResetScreen()
    # TODO(igushev): Draw screen main element, like ButtonBar, MainMenu, ContextMenu, MainButton
    if screen.HasElement(fase.MAIN_MENU_ID):
      self.DrawMainMenu([fase.MAIN_MENU_ID], screen.PopElement(fase.MAIN_MENU_ID))
    if screen.HasElement(fase.MAIN_BUTTON_ID):
      self.DrawMainButton([fase.MAIN_BUTTON_ID], screen.PopElement(fase.MAIN_BUTTON_ID), ui_imp_window)
    if screen.HasElement(fase.BUTTON_BAR_ID):
      self.DrawButtonBar([fase.BUTTON_BAR_ID], screen.PopElement(fase.BUTTON_BAR_ID), ui_imp_window)
    if screen.HasElement(fase.NEXT_STEP_BUTTON_ID):
      self.DrawNextStepButton([fase.NEXT_STEP_BUTTON_ID], screen.PopElement(fase.NEXT_STEP_BUTTON_ID), ui_imp_window)
    if screen.HasElement(fase.PREV_STEP_BUTTON_ID):
      self.DrawPrevStepButton([fase.PREV_STEP_BUTTON_ID], screen.PopElement(fase.PREV_STEP_BUTTON_ID), ui_imp_window)
    if screen.HasElement(fase.CONTEXT_MENU_ID):
      self.DrawContextMenu([fase.CONTEXT_MENU_ID], screen.PopElement(fase.CONTEXT_MENU_ID))
    self.DrawBaseElementsContainer([], screen, ui_imp_window)

  def DrawMainMenu(self, id_list, main_menu_element):
    # TODO(igushev): Draw actual main menu.
    for menu_item_id, menu_item_element in main_menu_element.GetIdElementList():
      self.ui_imp.DrawMenuItem(self, id_list + [menu_item_id], menu_item_element)

  def DrawMainButton(self, id_list, main_button_element, ui_imp_parent):
    # TODO(igushev): Draw actual main button.
    self.ui_imp.DrawButton(self, id_list, main_button_element, ui_imp_parent)

  def DrawButtonBar(self, id_list, button_bar_element, ui_imp_parent):
    # TODO(igushev): Draw actual button bar.
    # NOTE(igushev): Button Bar Layout will have id_list of Button Bar.
    ui_imp_element = self.ui_imp.DrawLayout(self, id_list, button_bar_element, ui_imp_parent)
    for button_id, button_element in button_bar_element.GetIdElementList():
      self.DrawButton(id_list + [button_id], button_element, ui_imp_element)

  def DrawNextStepButton(self, id_list, next_step_button_element, ui_imp_parent):
    # TODO(igushev): Draw actual next button.
    next_step_button_element.SetText('Next')
    self.ui_imp.DrawButton(self, id_list, next_step_button_element, ui_imp_parent)

  def DrawPrevStepButton(self, id_list, prev_step_button_element, ui_imp_parent):
    # TODO(igushev): Draw actual prev button.
    prev_step_button_element.SetText('Previous')
    self.ui_imp.DrawButton(self, id_list, prev_step_button_element, ui_imp_parent)

  def DrawContextMenu(self, id_list, context_menu_element):
    # TODO(igushev): Draw actual context menu.
    for menu_item_id, menu_item_element in context_menu_element.GetIdElementList():
      self.ui_imp.DrawMenuItem(self, id_list + [menu_item_id], menu_item_element)

  def DrawBaseElementsContainer(self, id_list, parent_element, ui_imp_parent):
    for id_, element in parent_element.GetIdElementList():
      self._DispatchDraw(id_list + [id_], element, ui_imp_parent)

  def _DispatchDraw(self, id_list, element, ui_imp_parent):
    if isinstance(element, fase.Layout):
      self.DrawLayout(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Label):
      self.DrawLabel(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Text):
      self.DrawText(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Image):
      self.DrawImage(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Button):
      self.DrawButton(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Variable):
      pass
    else:
      raise AssertionError('Unknown element type %s' % type(element))

  def DrawLayout(self, id_list, layout_element, ui_imp_parent):
    ui_imp_element = self.ui_imp.DrawLayout(self, id_list, layout_element, ui_imp_parent)
    self.DrawBaseElementsContainer(id_list, layout_element, ui_imp_element)

  def DrawLabel(self, id_list, label_element, ui_imp_parent):
    self.ui_imp.DrawLabel(self, id_list, label_element, ui_imp_parent)

  def DrawText(self, id_list, text_element, ui_imp_parent):
    self.ui_imp.DrawText(self, id_list, text_element, ui_imp_parent)

  def DrawImage(self, id_list, image_element, ui_imp_parent):
    self.ui_imp.DrawImage(self, id_list, image_element, ui_imp_parent)

  def DrawButton(self, id_list, button_element, ui_imp_parent):
    self.ui_imp.DrawButton(self, id_list, button_element, ui_imp_parent)

  def Run(self):
    self.ui_imp.Run()

  def ElementClicked(self, id_list):
    self.client.ElementClicked(id_list, self.id_list_to_value)

  def ElementUpdated(self, id_list, value):
    self.id_list_to_value[tuple(id_list)] = value
