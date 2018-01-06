import tkinter


class ClickCallBack(object):
  
  def __init__(self, ui_tk, id_list):
    self.ui_tk = ui_tk
    self.id_list = id_list 

  def __call__(self):
    self.ui_tk.ElementClicked(self.id_list)


class UpdateCallBack(object):
  
  def __init__(self, ui_tk, id_list):
    self.ui_tk = ui_tk
    self.id_list = id_list 

  def __call__(self, *args):
    self.ui_tk.ElementUpdated(self.id_list, *args)


class FaseTkUIImp(object):

  def __init__(self):
    self.ui_imp_root = tkinter.Tk()
    self.ui_imp_root.option_add('*tearOff', False)
    self.ui_imp_root.geometry('480x640+50+50')
    self.ui_imp_root.resizable(False, False)
    self.ui_imp_frame = tkinter.Frame(self.ui_imp_root)
    self.main_menu = tkinter.Menu(self.ui_imp_root)
    self.ui_imp_root['menu'] = self.main_menu
    self.id_list_to_var = dict()

  def SetUI(self, ui):
    self.ui = ui

  def ResetScreen(self):
    self.ui_imp_frame.destroy()
    self.ui_imp_frame = tkinter.Frame(self.ui_imp_root)
    self.ui_imp_frame.grid()
    self.main_menu.destroy()
    self.main_menu = tkinter.Menu(self.ui_imp_root)
    self.ui_imp_root['menu'] = self.main_menu
    self.id_list_to_var = dict()
    return self.ui_imp_frame

  def DrawMenuItem(self, ui, id_list, menu_item_element):
    self.main_menu.add_command(label=menu_item_element.GetText(), command=ClickCallBack(self, id_list))

  def DrawLayout(self, ui, id_list, layout_element, ui_imp_parent):
    layout = tkinter.Frame(ui_imp_parent)
    layout.grid()
    return layout

  def DrawLabel(self, ui, id_list, label_element, ui_imp_parent):
    label = tkinter.Label(ui_imp_parent, text=label_element.GetLabel())
    label.grid()
    return label

  def DrawText(self, ui, id_list, text_element, ui_imp_parent):
    var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = var
    var.trace('w', UpdateCallBack(self, id_list))
    text = tkinter.Entry(ui_imp_parent, textvariable=var)
    text.grid()
    return text

  def DrawImage(self, ui, id_list, image_element, ui_imp_parent):
    # TODO(igushev): Draw actual image.
    label = tkinter.Label(ui_imp_parent, text=image_element.GetImage())
    label.grid()
    return label 

  def DrawButton(self, ui, id_list, button_element, ui_imp_parent):
    button = tkinter.Button(ui_imp_parent, text=button_element.GetText(), command=ClickCallBack(self, id_list))
    button.grid()
    return button

  def Run(self):
    self.ui_imp_root.mainloop()

  def ElementClicked(self, id_list):
    self.ui.ElementClicked(id_list)

  def ElementUpdated(self, id_list, *args):
    value = self.id_list_to_var[tuple(id_list)].get() 
    self.ui.ElementUpdated(id_list, value)
