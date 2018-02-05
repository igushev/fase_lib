import fase


BUILT_IN_IDS = set([fase.NEXT_STEP_BUTTON_ID,
                    fase.PREV_STEP_BUTTON_ID,
                    fase.CONTEXT_MENU_ID,
                    fase.POPUP_ID,
                    fase.MAIN_MENU_ID,
                    fase.MAIN_BUTTON_ID,
                    fase.BUTTON_BAR_ID])


class FaseUI(object):

  def __init__(self, ui_imp):
    self.ui_imp = ui_imp
    self.ui_imp.SetUI(self)

  def SetClient(self, client):
    self.client = client

  def DrawScreen(self, screen):
    ui_imp_window = self.ui_imp.ResetScreen(scrollable=screen.GetScrollable())
    self.DrawMainContextMenusNextPrevButtons(screen)
    self.DrawMainButtonAndNavigationButtons(screen)
    self.DrawBaseElementsContainer([], screen, ui_imp_window)

  def DrawMainContextMenusNextPrevButtons(self, screen):
    main_menu_element = screen.GetElement(fase.MAIN_MENU_ID) if screen.HasElement(fase.MAIN_MENU_ID) else None
    context_menu_element = screen.GetElement(fase.CONTEXT_MENU_ID) if screen.HasElement(fase.CONTEXT_MENU_ID) else None
    next_button_element = (screen.GetElement(fase.NEXT_STEP_BUTTON_ID)
                           if screen.HasElement(fase.NEXT_STEP_BUTTON_ID) else None)
    prev_button_element = (screen.GetElement(fase.PREV_STEP_BUTTON_ID)
                           if screen.HasElement(fase.PREV_STEP_BUTTON_ID) else None)
    self.ui_imp.PrepareScreenMainContextMenusNextPrevButtons(
        main_menu=main_menu_element is not None, context_menu=context_menu_element is not None,
        next_button=next_button_element is not None, prev_button=prev_button_element is not None,
        title=screen.GetTitle())
    if main_menu_element:
      for menu_item_id, menu_item_element in main_menu_element.GetIdElementList():
        self.ui_imp.DrawScreenMainMenuItem([fase.MAIN_MENU_ID, menu_item_id], menu_item_element)
    if context_menu_element:
      for menu_item_id, menu_item_element in context_menu_element.GetIdElementList():
        self.ui_imp.DrawScreenContextMenuItem([fase.CONTEXT_MENU_ID, menu_item_id], menu_item_element)
    if next_button_element:
      self.ui_imp.DrawScreenNextStepButton([fase.NEXT_STEP_BUTTON_ID], next_button_element)
    if prev_button_element:
      self.ui_imp.DrawScreenPrevStepButton([fase.PREV_STEP_BUTTON_ID], prev_button_element)

  def DrawMainButtonAndNavigationButtons(self, screen):
    main_button_element = screen.GetElement(fase.MAIN_BUTTON_ID) if screen.HasElement(fase.MAIN_BUTTON_ID) else None
    button_bar_element = screen.GetElement(fase.BUTTON_BAR_ID) if screen.HasElement(fase.BUTTON_BAR_ID) else None 
    nav_button_id_element_list = button_bar_element.GetIdElementList() if button_bar_element else []
    self.ui_imp.PrepareScreenMainButtonAndNavigationButtons(
        main_button=main_button_element is not None, nav_button_num=len(nav_button_id_element_list))
    if main_button_element:
      ui_imp_main_button = self.ui_imp.DrawScreenMainButton([fase.MAIN_BUTTON_ID], main_button_element)
      if main_button_element.GetContextMenu():
        for menu_item_id, menu_item_element in main_button_element.GetContextMenu().GetIdElementList():
          self.ui_imp.DrawContextMenuItem(
              [fase.MAIN_BUTTON_ID, fase.CONTEXT_MENU_ID, menu_item_id], menu_item_element, ui_imp_main_button)
    # NOTE(igushev): Button Bar Layout will have id_list of Button Bar.
    for nav_button_i, (nav_button_id, nav_button_element) in enumerate(nav_button_id_element_list):
      self.ui_imp.DrawScreenNavButton([fase.BUTTON_BAR_ID, nav_button_id], nav_button_element, nav_button_i)

  def DrawBaseElementsContainer(self, id_list, parent_element, ui_imp_parent):
    for id_, element in parent_element.GetIdElementList():
      if id_ in BUILT_IN_IDS:
        continue
      self._DispatchDraw(id_list + [id_], element, ui_imp_parent)

  def _DispatchDraw(self, id_list, element, ui_imp_parent):
    if isinstance(element, fase.Layout):
      self.DrawLayout(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Label):
      self.DrawLabel(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Text):
      self.DrawText(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Switch):
      self.DrawSwitch(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Image):
      self.DrawImage(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.Button):
      self.DrawButton(id_list, element, ui_imp_parent)
    elif isinstance(element, fase.ContactPicker):
      self.DrawContactPicker(id_list, element, ui_imp_parent)
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

  def DrawSwitch(self, id_list, switch_element, ui_imp_parent):
    self.ui_imp.DrawSwitch(id_list, switch_element, ui_imp_parent)

  def DrawImage(self, id_list, image_element, ui_imp_parent):
    self.ui_imp.DrawImage(id_list, image_element, ui_imp_parent)

  def DrawButton(self, id_list, button_element, ui_imp_parent):
    ui_imp_button = self.ui_imp.DrawButton(id_list, button_element, ui_imp_parent)
    if button_element.GetContextMenu():
      for menu_item_id, menu_item_element in button_element.GetContextMenu().GetIdElementList():
        self.ui_imp.DrawContextMenuItem(
            id_list + [fase.CONTEXT_MENU_ID, menu_item_id], menu_item_element, ui_imp_button)

  def DrawContactPicker(self, id_list, contact_picker_element, ui_imp_parent):
    self.ui_imp.DrawContactPicker(id_list, contact_picker_element, ui_imp_parent)

  def ShowPopup(self, popup):
    assert len(popup.GetIdElementList()) == 1
    button_id, button_element = popup.GetIdElementList()[0]
    assert button_element.GetText() == 'OK'
    self.ui_imp.ShowPopup(popup)
    return [fase.POPUP_ID, button_id]

  def Run(self):
    self.ui_imp.Run()

  def ElementUpdatedCallBack(self, id_list, value):
    self.client.ElementUpdated(id_list, value)

  def ScreenUpdateCallBack(self):
    self.client.ScreenUpdate()

  def ElementClickedCallBack(self, id_list):
    self.client.ElementClicked(id_list)

  def ElementUpdatedReceived(self, id_list, value):
    self.ui_imp.ElementUpdatedReceived(id_list, value)
