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
    ui_imp_window = self.ui_imp.ResetScreen(scrollable=screen.GetScrollable())
    self.DrawMainContextMenusNextPrevButtons(screen)
    self.DrawMainButtonAndNavigationButtons(screen)
    self.DrawBaseElementsContainer([], screen, ui_imp_window)

  def DrawMainContextMenusNextPrevButtons(self, screen):
    main_menu_element = screen.PopElement(fase.MAIN_MENU_ID) if screen.HasElement(fase.MAIN_MENU_ID) else None
    context_menu_element = screen.PopElement(fase.CONTEXT_MENU_ID) if screen.HasElement(fase.CONTEXT_MENU_ID) else None
    next_button_element = (screen.PopElement(fase.NEXT_STEP_BUTTON_ID)
                           if screen.HasElement(fase.NEXT_STEP_BUTTON_ID) else None)
    prev_button_element = (screen.PopElement(fase.PREV_STEP_BUTTON_ID)
                           if screen.HasElement(fase.PREV_STEP_BUTTON_ID) else None)
    self.ui_imp.PrepareMainContextMenusNextPrevButtons(
        main_menu=main_menu_element is not None, context_menu=context_menu_element is not None,
        next_button=next_button_element is not None, prev_button=prev_button_element is not None,
        title=screen.GetTitle())
    if main_menu_element:
      for menu_item_id, menu_item_element in main_menu_element.GetIdElementList():
        self.ui_imp.DrawMainMenuItem([fase.MAIN_MENU_ID, menu_item_id], menu_item_element)
    if context_menu_element:
      for menu_item_id, menu_item_element in context_menu_element.GetIdElementList():
        self.ui_imp.DrawContextMenuItem([fase.CONTEXT_MENU_ID, menu_item_id], menu_item_element)
    if next_button_element:
      self.ui_imp.DrawNextStepButton([fase.NEXT_STEP_BUTTON_ID], next_button_element)
    if prev_button_element:
      self.ui_imp.DrawPrevStepButton([fase.PREV_STEP_BUTTON_ID], prev_button_element)

  def DrawMainButtonAndNavigationButtons(self, screen):
    main_button_element = screen.PopElement(fase.MAIN_BUTTON_ID) if screen.HasElement(fase.MAIN_BUTTON_ID) else None
    button_bar_element = screen.PopElement(fase.BUTTON_BAR_ID) if screen.HasElement(fase.BUTTON_BAR_ID) else None 
    nav_button_id_element_list = button_bar_element.GetIdElementList() if button_bar_element else []
    self.ui_imp.PrepareMainButtonAndNavigationButtons(
        main_button=main_button_element is not None, nav_button_num=len(nav_button_id_element_list))
    if main_button_element:
      self.ui_imp.DrawMainButton([fase.MAIN_BUTTON_ID], main_button_element)
    # NOTE(igushev): Button Bar Layout will have id_list of Button Bar.
    for nav_button_i, (nav_button_id, nav_button_element) in enumerate(nav_button_id_element_list):
      self.ui_imp.DrawNavButton([fase.BUTTON_BAR_ID, nav_button_id], nav_button_element, nav_button_i)

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
    ui_imp_element = self.ui_imp.DrawLayout(id_list, layout_element, ui_imp_parent)
    self.DrawBaseElementsContainer(id_list, layout_element, ui_imp_element)

  def DrawLabel(self, id_list, label_element, ui_imp_parent):
    self.ui_imp.DrawLabel(id_list, label_element, ui_imp_parent)

  def DrawText(self, id_list, text_element, ui_imp_parent):
    self.ui_imp.DrawText(id_list, text_element, ui_imp_parent)

  def DrawImage(self, id_list, image_element, ui_imp_parent):
    self.ui_imp.DrawImage(id_list, image_element, ui_imp_parent)

  def DrawButton(self, id_list, button_element, ui_imp_parent):
    self.ui_imp.DrawButton(id_list, button_element, ui_imp_parent)

  # TODO(igushev): Add better support for popups.
  def ShowPopup(self, popup):
    assert len(popup.GetIdElementList()) == 1
    button_id, button_element = popup.GetIdElementList()[0]
    assert button_element.GetText() == 'OK'
    self.ui_imp.ShowPopup(popup)
    return [fase.POPUP_ID, button_id]

  def Run(self):
    self.ui_imp.Run()

  def ElementUpdatedCallBack(self, id_list, value):
    self.id_list_to_value[tuple(id_list)] = value

  def ElementsUpdateReceived(self, id_list_to_value):
    for id_list_update, value in id_list_to_value.items():
      self.ui_imp.ElementUpdatedReceived(id_list_update, value)

  def ScreenUpdateCallBack(self):
    self.client.ScreenUpdate(self.id_list_to_value)

  def ElementClickedCallBack(self, id_list):
    self.client.ElementClicked(id_list, self.id_list_to_value)
