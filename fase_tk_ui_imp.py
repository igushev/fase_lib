import math
import tkinter
from tkinter import font, messagebox

import fase

ROOT_SIZE = '540x960+50+50'
MAIN_MENU_TEXT = '|||'
CONTEXT_MENU_TEXT = '...'
NAV_BUTTON_WIDTH = 75
NAV_BUTTON_HEIGHT = 40
MAIN_BUTTON_WIDTH = 75
MAIN_BUTTON_HEIGHT = 75


class ClickCallBack(object):
  
  def __init__(self, ui_tk, id_list):
    self.ui_tk = ui_tk
    self.id_list = id_list 

  def __call__(self, *args):
    self.ui_tk.ElementClicked(self.id_list)


class UpdateCallBack(object):
  
  def __init__(self, ui_tk, id_list):
    self.ui_tk = ui_tk
    self.id_list = id_list 

  def __call__(self, *args):
    self.ui_tk.ElementUpdated(self.id_list, *args)


class ParentElement(object):
  
  def __init__(self, ui_imp_parent, orientation, click_callback=None):
    self._ui_imp_parent = ui_imp_parent
    self._orientation = orientation
    self._click_callback = click_callback
    self._column = 0
    self._row = 0

  def GetUIImpParent(self):
    return self._ui_imp_parent

  def GetOrientation(self):
    return self._orientation

  def GetClickCallBack(self):
    return self._click_callback

  def GetColumn(self):
    return self._column

  def GetRow(self):
    return self._row

  def Next(self):
    if self._orientation == fase.Layout.VERTICAL:
      self._row += 1
    elif self._orientation == fase.Layout.HORIZONTAL:
      self._column += 1
    else:
      raise ValueError(self._orientation)


class FaseTkUIImp(object):

  def __init__(self):
    self.ui_imp_root = tkinter.Tk()
    self.ui_imp_root.option_add('*tearOff', False)
    self.ui_imp_root.geometry(ROOT_SIZE)
    self.ui_imp_root.resizable(False, False)
    self.ui_imp_root.columnconfigure(0, weight=1)
    self.ui_imp_root.rowconfigure(0, weight=1)
    self.ui_imp_frame = None

  def InitScreen(self, scrollable=False):
    self.ui_imp_frame = tkinter.Frame(self.ui_imp_root)
    self.ui_imp_frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
    # Middle layout take entire space.
    self.ui_imp_frame.columnconfigure(0, weight=1)
    self.ui_imp_frame.rowconfigure(1, weight=1)
    
    if scrollable:
      ui_imp_middle_layout = tkinter.Frame(self.ui_imp_frame)
      ui_imp_middle_layout.grid(row=1, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
      # Canvas take entire space and Scrollbar entire height.
      ui_imp_middle_layout.columnconfigure(0, weight=1)
      ui_imp_middle_layout.rowconfigure(0, weight=1)
  
      ui_imp_widget_canvas = tkinter.Canvas(ui_imp_middle_layout)
      ui_imp_widget_canvas.grid(column=0, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
      
      ui_imp_widget_scrollbar = tkinter.Scrollbar(
          ui_imp_middle_layout, orient=tkinter.VERTICAL, command=ui_imp_widget_canvas.yview)
      ui_imp_widget_canvas.configure(yscrollcommand=ui_imp_widget_scrollbar.set)
      ui_imp_widget_scrollbar.grid(column=1, row=0, sticky=(tkinter.N, tkinter.S))
      
      def OnWidgetLayoutConfigure(event):
        ui_imp_widget_canvas.configure(scrollregion=ui_imp_widget_canvas.bbox(tkinter.ALL))
        ui_imp_width_layout.config(width=ui_imp_widget_canvas.winfo_width())
    
      ui_imp_widget_layout = tkinter.Frame(ui_imp_widget_canvas)
      ui_imp_widget_canvas.create_window((0,0), window=ui_imp_widget_layout, anchor='nw')
      ui_imp_widget_layout.bind("<Configure>", OnWidgetLayoutConfigure)
      ui_imp_width_layout = tkinter.Frame(ui_imp_widget_layout)
      ui_imp_width_layout.grid()
    else:
      ui_imp_widget_layout = tkinter.Frame(self.ui_imp_frame)
      ui_imp_widget_layout.grid(row=1, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
      ui_imp_widget_layout.columnconfigure(0, weight=1)
      

    self.id_list_to_var = dict()
    return ParentElement(ui_imp_widget_layout, fase.Layout.VERTICAL)

  def SetUI(self, ui):
    self.ui = ui

  def ResetScreen(self, scrollable=False):
    if self.ui_imp_frame:
      self.ui_imp_frame.destroy()
    return self.InitScreen(scrollable=scrollable)

  def PrepareMainContextMenusNextPrevButtons(
      self, main_menu=False, context_menu=False, next_button=False, prev_button=False, title=None):
    if not (main_menu or context_menu or next_button or prev_button or title):
      return
    ui_imp_header_layout = tkinter.Frame(self.ui_imp_frame)
    ui_imp_header_layout.grid(row=0, sticky=(tkinter.W, tkinter.E))

    side_button_num = max(int(main_menu) + int(prev_button), int(context_menu) + int(next_button))
    total_column_num = side_button_num * 2 + 1
    ui_imp_button_frame_list = []
    for column_i in range(total_column_num):
      if column_i == side_button_num:
        # Header label take entire space.
        ui_imp_header_layout.columnconfigure(column_i, weight=1)
        if title is not None:
          ui_imp_header_label = tkinter.Label(ui_imp_header_layout, text=title)
          ui_imp_header_label.grid(column=column_i, row=0)
      else:
        ui_imp_button_frame = tkinter.Frame(ui_imp_header_layout, width=NAV_BUTTON_WIDTH, height=NAV_BUTTON_HEIGHT)
        ui_imp_button_frame.grid_propagate(False)
        ui_imp_button_frame.grid(column=column_i, row=0)
        ui_imp_button_frame.columnconfigure(0, weight=1)
        ui_imp_button_frame.rowconfigure(0, weight=1)
        ui_imp_button_frame_list.append(ui_imp_button_frame)

    if main_menu:
      self.ui_imp_main_menu = tkinter.Menu()
      ui_imp_main_menu_button = tkinter.Button(ui_imp_button_frame_list[0], text=MAIN_MENU_TEXT)
      ui_imp_main_menu_button.grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
      ui_imp_main_menu_button.bind('<1>', lambda e: self.ui_imp_main_menu.post(e.x_root, e.y_root))
    else:
      self.ui_imp_main_menu = None

    if context_menu:
      self.ui_imp_context_menu = tkinter.Menu()
      # Either -1 or -2.
      ui_imp_context_menu_button = tkinter.Button(ui_imp_button_frame_list[-1-int(next_button)], text=CONTEXT_MENU_TEXT)
      ui_imp_context_menu_button.grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
      ui_imp_context_menu_button.bind('<1>', lambda e: self.ui_imp_context_menu.post(e.x_root, e.y_root))
    else:
      self.ui_imp_context_menu = None

    if prev_button:
      self.ui_imp_prev_button_frame = ui_imp_button_frame_list[int(main_menu)]  # Either 0 or 1.
    else:
      self.ui_imp_prev_button_frame = None

    if next_button:
      self.ui_imp_next_button_frame = ui_imp_button_frame_list[-1]
    else:
      self.ui_imp_next_button_frame = None

  def DrawMainMenuItem(self, id_list, menu_item_element):
    self.ui_imp_main_menu.add_command(
        label=menu_item_element.GetText(),
        command=ClickCallBack(self, id_list) if menu_item_element.GetOnClick() is not None else None)

  def DrawContextMenuItem(self, id_list, menu_item_element):
    assert menu_item_element.GetOnClick() is not None
    self.ui_imp_context_menu.add_command(label=menu_item_element.GetText(), command=ClickCallBack(self, id_list))

  def DrawNextStepButton(self, id_list, next_step_button_element):
    assert next_step_button_element.GetOnClick() is not None
    tkinter.Button(self.ui_imp_next_button_frame, text=next_step_button_element.GetText(),
                   command=ClickCallBack(self, id_list)).grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

  def DrawPrevStepButton(self, id_list, prev_step_button_element):
    assert prev_step_button_element.GetOnClick() is not None
    tkinter.Button(self.ui_imp_prev_button_frame, text=prev_step_button_element.GetText(),
                   command=ClickCallBack(self, id_list)).grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

  def PrepareMainButtonAndNavigationButtons(self, main_button=False, nav_button_num=0):
    if not (main_button or nav_button_num):
      return
    if main_button:
      total_button_num = math.ceil(nav_button_num / 2) * 2 + int(main_button)
      main_button_i = math.ceil(nav_button_num / 2)
    else:
      total_button_num = nav_button_num
      main_button_i = None

    ui_imp_footer_layout = tkinter.Frame(self.ui_imp_frame)
    ui_imp_footer_layout.grid(row=2, sticky=(tkinter.W, tkinter.E))
    self.ui_imp_main_button_frame = None
    self.ui_imp_nav_button_frame_list = []
    for button_i in range(total_button_num):
      if button_i == main_button_i:
        ui_imp_button_frame = tkinter.Frame(ui_imp_footer_layout, width=MAIN_BUTTON_WIDTH, height=MAIN_BUTTON_HEIGHT)
      else: 
        ui_imp_button_frame = tkinter.Frame(ui_imp_footer_layout, width=NAV_BUTTON_WIDTH, height=NAV_BUTTON_HEIGHT)
      ui_imp_button_frame.grid_propagate(False)
      ui_imp_button_frame.grid(column=button_i, row=0)
      ui_imp_button_frame.columnconfigure(0, weight=1)
      ui_imp_button_frame.rowconfigure(0, weight=1)
      ui_imp_footer_layout.columnconfigure(button_i, weight=1)
      if button_i == main_button_i:
        self.ui_imp_main_button_frame = ui_imp_button_frame
      else:
        self.ui_imp_nav_button_frame_list.append(ui_imp_button_frame)
      
  def DrawMainButton(self, id_list, main_button_element):
    assert self.ui_imp_main_button_frame is not None
    assert main_button_element.GetOnClick() is not None
    tkinter.Button(self.ui_imp_main_button_frame, text=main_button_element.GetText(),
                   command=ClickCallBack(self, id_list)).grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

  def DrawNavButton(self, id_list, nav_button_element, nav_button_i):
    assert nav_button_element.GetOnClick() is not None
    tkinter.Button(self.ui_imp_nav_button_frame_list[nav_button_i], text=nav_button_element.GetText(),
                   command=ClickCallBack(self, id_list)).grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

  def _ConfigureParent(self, ui_imp_parent, maximize=False):
    if maximize:
      if ui_imp_parent.GetOrientation() == fase.Layout.VERTICAL:
        ui_imp_parent.GetUIImpParent().rowconfigure(ui_imp_parent.GetRow(), weight=1)
      elif ui_imp_parent.GetOrientation() == fase.Layout.HORIZONTAL:
        ui_imp_parent.GetUIImpParent().columnconfigure(ui_imp_parent.GetColumn(), weight=1)
      else:
        raise ValueError(self._orientation)

  def DrawLayout(self, id_list, layout_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent, maximize=(layout_element.GetSize()==fase.Layout.MAX))
    ui_imp_layout = tkinter.Frame(ui_imp_parent.GetUIImpParent())
    ui_imp_layout.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                       sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

    if layout_element.GetOrientation() == fase.Layout.VERTICAL:
      ui_imp_layout.columnconfigure(ui_imp_parent.GetColumn(), weight=1)
    elif layout_element.GetOrientation() == fase.Layout.HORIZONTAL:
      ui_imp_layout.rowconfigure(ui_imp_parent.GetRow(), weight=1)
    else:
      raise ValueError(self._orientation)

    click_callback = None
    if layout_element.GetOnClick():
      click_callback = ClickCallBack(self, id_list)
    elif ui_imp_parent.GetClickCallBack():
      click_callback = ui_imp_parent.GetClickCallBack()

    if click_callback is not None:
      ui_imp_layout.bind('<1>', click_callback)

    ui_imp_parent.Next()
    return ParentElement(ui_imp_layout, layout_element.GetOrientation(), click_callback=click_callback)

  def DrawLabel(self, id_list, label_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent, maximize=(label_element.GetSize()==fase.Label.MAX))
    ui_imp_label = tkinter.Label(ui_imp_parent.GetUIImpParent(), text=label_element.GetLabel())

    if label_element.GetFont() is not None:
      label_font = font.Font(font=ui_imp_label['font'])
      label_font.configure(size=int(label_font.actual()['size']*label_element.GetFont()))
      ui_imp_label.configure(font=label_font)

    if label_element.GetAlight() is not None:
      if label_element.GetAlight() == fase.Label.LEFT:
        anchor = 'w'
      elif label_element.GetAlight() == fase.Label.RIGHT:
        anchor = 'e'
      elif label_element.GetAlight() == fase.Label.CENTER:
        anchor = 'center'
      ui_imp_label.configure(anchor=anchor)

    click_callback = None
    if label_element.GetOnClick():
      click_callback = ClickCallBack(self, id_list)
    elif ui_imp_parent.GetClickCallBack():
      click_callback = ui_imp_parent.GetClickCallBack()

    if click_callback is not None:
      ui_imp_label.bind('<1>', click_callback)

    ui_imp_label.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                      sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ui_imp_label

  def DrawText(self, id_list, text_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    if text_element.GetText() is not None:
      ui_imp_var.set(text_element.GetText())
    self.id_list_to_var[tuple(id_list)] = ui_imp_var
    ui_imp_var.trace('w', UpdateCallBack(self, id_list))
    ui_imp_text = tkinter.Entry(ui_imp_parent.GetUIImpParent(), textvariable=ui_imp_var)
    ui_imp_text.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                     sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ui_imp_text

  def DrawImage(self, id_list, image_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_photo = tkinter.PhotoImage(file=image_element.GetImage())
    ui_imp_label = tkinter.Label(ui_imp_parent.GetUIImpParent(), image=ui_imp_photo)
    ui_imp_label.image = ui_imp_photo 
    ui_imp_label.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow())
    ui_imp_parent.Next()
    return ui_imp_label 

  def DrawButton(self, id_list, button_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_button = tkinter.Button(ui_imp_parent.GetUIImpParent(), text=button_element.GetText())

    if button_element.GetOnClick():
      ui_imp_button.configure(command=ClickCallBack(self, id_list))

    ui_imp_button.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow())
    ui_imp_parent.Next()
    return ui_imp_button

  def ShowPopup(self, popup):
    messagebox.showinfo(message=popup.GetText())

  def Run(self):
    self.ui_imp_root.mainloop()

  def ElementClicked(self, id_list):
    self.ui.ElementClicked(id_list)

  def ElementUpdated(self, id_list, *args):
    value = self.id_list_to_var[tuple(id_list)].get() 
    self.ui.ElementUpdated(id_list, value)
