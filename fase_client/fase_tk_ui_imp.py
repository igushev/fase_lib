import math
import datetime
import tkinter
from tkinter import font, messagebox, ttk
from PIL import ImageTk, Image
import re

from fase import fase


ROOT_SIZE = '540x960+50+50'
MAIN_MENU_TEXT = '|||'
CONTEXT_MENU_TEXT = '...'
TITLE_FONT = 2
NAV_BUTTON_WIDTH = 75
NAV_BUTTON_HEIGHT = 40
MAIN_BUTTON_WIDTH = 75
MAIN_BUTTON_HEIGHT = 75
SCREEN_UPDATE_INTERVAL = 200

REFRESH_BUTTON_TEXT = 'Refresh'
ON_MORE_BUTTON_TEXT = 'More'

BUTTON_TEXT_LIST_TO_INFO_TYPE = {('ok', ): messagebox.OK,
                                 ('ok', 'cancel'): messagebox.OKCANCEL,
                                 ('yes', 'no'): messagebox.YESNO,
                                 ('yes', 'no', 'cancel'): messagebox.YESNOCANCEL,
                                 ('retry', 'cancel'): messagebox.RETRYCANCEL,
                                 ('abort', 'retry', 'ignore'): messagebox.ABORTRETRYIGNORE}

CONTACT_FORMAT = '{display_name}|{phone_number}'
CONTACT_REGEXP = '(?P<display_name>.*)\|(?P<phone_number>.*)'

DATETIME_TYPE_TO_FORMAT = {fase.DateTimePicker.DATE: '%Y-%m-%d',
                           fase.DateTimePicker.TIME: '%H:%M:%S',
                           fase.DateTimePicker.DATETIME: '%Y-%m-%d %H:%M:%S'}

PLACE_FORMAT = '{google_place_id}|{city}|{state}|{country}'
PLACE_REGEXP = '(?P<google_place_id>.*)\|(?P<city>.*)\|(?P<state>.*)\|(?P<country>.*)'


class ElementUpdatedCallback(object):
  
  def __init__(self, ui_tk, id_list):
    self.ui_tk = ui_tk
    self.id_list = id_list 

  def __call__(self, *args):
    self.ui_tk.ElementUpdated(self.id_list)


class ElementCallbackCallback(object):
  
  def __init__(self, ui_tk, id_list, method):
    self.ui_tk = ui_tk
    self.id_list = id_list
    self.method = method

  def __call__(self, *args):
    self.ui_tk.ElementCallback(self.id_list, self.method)


class ElementUpdatedAndCallbackCallback(object):
  
  def __init__(self, ui_tk, id_list, method):
    self.ui_tk = ui_tk
    self.id_list = id_list
    self.method = method

  def __call__(self, *args):
    self.ui_tk.ElementUpdated(self.id_list)
    self.ui_tk.ElementCallback(self.id_list, self.method)


class ElementVariable(object):
  
  def Update(self, value):
    raise NotImplementedError()


class TextElementVariable(object):

  def __init__(self, ui_imp_var):
    self._ui_imp_var = ui_imp_var

  def Get(self):
    value = self._ui_imp_var.get()
    return value if value else None  # Replace empty string with None.

  def Update(self, value):
    self._ui_imp_var.set(value if value is not None else '') 


class SwitchElementVariable(object):
  
  def __init__(self, ui_imp_var):
    self._ui_imp_var = ui_imp_var

  def Get(self):
    return self._ui_imp_var.get()

  def Update(self, value):
    self._ui_imp_var.set(value) 


class SelectElementVariable(object):
  
  def __init__(self, ui_imp_var):
    self._ui_imp_var = ui_imp_var

  def Get(self):
    return self._ui_imp_var.get()

  def Update(self, value):
    self._ui_imp_var.set(value) 



class SliderElementVariable(object):
  
  def __init__(self, ui_imp_var):
    self._ui_imp_var = ui_imp_var

  def Get(self):
    return str(self._ui_imp_var.get())

  def Update(self, value):
    self._ui_imp_var.set(float(value)) 


class ContactPickerElementVariable(object):

  def __init__(self, ui_imp_var):
    self._ui_imp_var = ui_imp_var

  def Get(self):
    displayed_value = self._ui_imp_var.get()
    if not displayed_value:  # Replace empty string with None.
      return None
    contact_match = re.match(CONTACT_REGEXP, displayed_value)
    contact = fase.Contact(
        display_name=contact_match.group('display_name') or None,
        phone_number=contact_match.group('phone_number') or None)
    value = contact.ToJSON()
    return value

  def Update(self, value):
    if value is not None:
      contact = fase.Contact.FromJSON(value)
      displayed_value = CONTACT_FORMAT.format(display_name=contact.display_name or '',
                                              phone_number=contact.phone_number or '')
    else:
      displayed_value = ''
    self._ui_imp_var.set(displayed_value)


class DateTimePickerElementVariable(object):

  def __init__(self, ui_imp_var, type_):
    self._ui_imp_var = ui_imp_var
    self._type = type_

  def Get(self):
    value = self._ui_imp_var.get()
    if not value:  # Replace empty string with None.
      return None
    datetime_format = DATETIME_TYPE_TO_FORMAT[self._type]
    return datetime.datetime.strptime(value, datetime_format).strftime(fase.DATETIME_FORMAT)

  def Update(self, value):
    if value is not None:
      datetime_format = DATETIME_TYPE_TO_FORMAT[self._type]
      displayed_value = datetime.datetime.strptime(value, fase.DATETIME_FORMAT).strftime(datetime_format)
    else:
      displayed_value = ''
    self._ui_imp_var.set(displayed_value) 


class PlacePickerElementVariable(object):

  def __init__(self, ui_imp_var, type_):
    self._ui_imp_var = ui_imp_var
    assert type_ == fase.PlacePicker.CITY

  def Get(self):
    displayed_value = self._ui_imp_var.get()
    if not displayed_value:  # Replace empty string with None.
      return None
    place_match = re.match(PLACE_REGEXP, displayed_value)
    place = fase.Place(
        google_place_id=place_match.group('google_place_id') or None,
        city=place_match.group('city') or None,
        state=place_match.group('state') or None,
        country=place_match.group('country') or None)
    value = place.ToJSON()
    return value

  def Update(self, value):
    if value is not None:
      place = fase.Place.FromJSON(value)
      displayed_value = PLACE_FORMAT.format(google_place_id=place.google_place_id or '',
                                            city=place.city or '',
                                            state=place.state or '',
                                            country=place.country or '')
    else:
      displayed_value = ''
    self._ui_imp_var.set(displayed_value)

class ParentElement(object):
  
  def __init__(self, ui_imp_parent, orientation=None, click_callback=None):
    self._ui_imp_parent = ui_imp_parent
    self._orientation = orientation
    self._click_callback = click_callback
    self._column = 0
    self._row = 0

  def GetUIImpParent(self):
    return self._ui_imp_parent

  def GetOrientation(self):
    return self._orientation

  def GetClickCallback(self):
    return self._click_callback

  def GetColumn(self):
    return self._column

  def GetRow(self):
    return self._row

  def Next(self):
    if self._orientation == fase.Frame.VERTICAL:
      self._row += 1
    elif self._orientation == fase.Frame.HORIZONTAL:
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
    self.element_updated_callback = True

  def InitScreen(self, scrollable=False):
    self.ui_imp_frame = tkinter.Frame(self.ui_imp_root)
    self.ui_imp_frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
    # Middle frame take entire space.
    self.ui_imp_frame.columnconfigure(0, weight=1)
    self.ui_imp_frame.rowconfigure(1, weight=1)
    
    if scrollable:
      ui_imp_middle_frame = tkinter.Frame(self.ui_imp_frame)
      ui_imp_middle_frame.grid(row=1, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
      # Canvas take entire space and Scrollbar entire height.
      ui_imp_middle_frame.columnconfigure(0, weight=1)
      ui_imp_middle_frame.rowconfigure(0, weight=1)
  
      ui_imp_widget_canvas = tkinter.Canvas(ui_imp_middle_frame)
      ui_imp_widget_canvas.grid(column=0, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
      
      ui_imp_widget_scrollbar = tkinter.Scrollbar(
          ui_imp_middle_frame, orient=tkinter.VERTICAL, command=ui_imp_widget_canvas.yview)
      ui_imp_widget_canvas.configure(yscrollcommand=ui_imp_widget_scrollbar.set)
      ui_imp_widget_scrollbar.grid(column=1, row=0, sticky=(tkinter.N, tkinter.S))
      
      def OnWidgetFrameConfigure(event):
        ui_imp_widget_canvas.configure(scrollregion=ui_imp_widget_canvas.bbox(tkinter.ALL))
        ui_imp_width_frame.config(width=ui_imp_widget_canvas.winfo_width())
    
      ui_imp_widget_frame = tkinter.Frame(ui_imp_widget_canvas)
      ui_imp_widget_canvas.create_window((0,0), window=ui_imp_widget_frame, anchor='nw')
      ui_imp_widget_frame.bind("<Configure>", OnWidgetFrameConfigure)
      ui_imp_width_frame = tkinter.Frame(ui_imp_widget_frame)
      ui_imp_width_frame.grid()
    else:
      ui_imp_widget_frame = tkinter.Frame(self.ui_imp_frame)
      ui_imp_widget_frame.grid(row=1, sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
      ui_imp_widget_frame.columnconfigure(0, weight=1)
      

    self.id_list_to_var = dict()
    return ParentElement(ui_imp_widget_frame, orientation=fase.Frame.VERTICAL)

  def SetUI(self, ui):
    self.ui = ui

  def ResetScreen(self, scrollable=False):
    if self.ui_imp_frame:
      self.ui_imp_frame.destroy()
    return self.InitScreen(scrollable=scrollable)

  def _ConfigureButton(self, id_list, button_element, ui_imp_button):
    if button_element.GetOnClick():
      ui_imp_button.configure(command=ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD))
      return ui_imp_button
    elif button_element.HasContextMenu():
      ui_imp_button_context_menu = tkinter.Menu()
      ui_imp_button.bind('<1>', lambda e: ui_imp_button_context_menu.post(e.x_root, e.y_root))
      return ui_imp_button_context_menu

  def _ConfigureButtonImage(self, button_image_element, ui_imp_button):
    if button_image_element is not None:
      ui_imp_photo = ImageTk.PhotoImage(Image.open(self.ui.GetResourceFilename(button_image_element.GetFilename())))
      ui_imp_button.ui_imp_photo = ui_imp_photo
      ui_imp_button.configure(image=ui_imp_photo, compound=tkinter.TOP)

  def _ConfigureMenuItemImage(self, menu_item_image_element, ui_imp_menu, index):
    if menu_item_image_element is not None:
      ui_imp_photo = ImageTk.PhotoImage(Image.open(self.ui.GetResourceFilename(menu_item_image_element.GetFilename())))
      setattr(ui_imp_menu, 'ui_imp_photo_%d' % index, ui_imp_photo)
      ui_imp_menu.entryconfigure(index=index, image=ui_imp_photo, compound=tkinter.TOP)

  def PrepareScreenMainContextMenusNextPrevButtons(
      self, main_menu=False, context_menu=False, next_button=False, prev_button=False, title=None, title_image=None):
    if not (main_menu or context_menu or next_button or prev_button or title or title_image):
      return
    ui_imp_header_frame = tkinter.Frame(self.ui_imp_frame)
    ui_imp_header_frame.grid(row=0, sticky=(tkinter.W, tkinter.E))

    side_button_num = max(int(main_menu) + int(prev_button), int(context_menu) + int(next_button))
    total_column_num = side_button_num * 2 + 1
    ui_imp_button_frame_list = []
    for column_i in range(total_column_num):
      if column_i == side_button_num:
        # Header label take entire space.
        ui_imp_header_frame.columnconfigure(column_i, weight=1)
        if title is not None or title_image is not None:
          assert int(title is not None) + int(title_image is not None)
          if title is not None:
            ui_imp_header_label = tkinter.Label(ui_imp_header_frame, text=title)
            label_font = font.Font(font=ui_imp_header_label['font'])
            label_font.configure(size=int(label_font.actual()['size']*TITLE_FONT))
            ui_imp_header_label.configure(font=label_font)
          else:
            ui_imp_header_photo = ImageTk.PhotoImage(Image.open(self.ui.GetResourceFilename(title_image.GetFilename())))
            ui_imp_header_label = tkinter.Label(ui_imp_header_frame, image=ui_imp_header_photo)
            ui_imp_header_label.image = ui_imp_header_photo
          ui_imp_header_label.grid(column=column_i, row=0)
      else:
        ui_imp_button_frame = tkinter.Frame(ui_imp_header_frame, width=NAV_BUTTON_WIDTH, height=NAV_BUTTON_HEIGHT)
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

  def DrawScreenMainMenuItem(self, id_list, menu_item_element, menu_item_image_element):
    self.ui_imp_main_menu.add_command(
        label=menu_item_element.GetText(),
        command=(ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD)
                 if menu_item_element.GetOnClick() is not None else None))
    self._ConfigureMenuItemImage(
        menu_item_image_element, self.ui_imp_main_menu, self.ui_imp_main_menu.index(tkinter.END))

  def DrawScreenContextMenuItem(self, id_list, menu_item_element, menu_item_image_element):
    assert menu_item_element.GetOnClick() is not None
    self.ui_imp_context_menu.add_command(
        label=menu_item_element.GetText(), command=ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD))
    self._ConfigureMenuItemImage(
        menu_item_image_element, self.ui_imp_context_menu, self.ui_imp_context_menu.index(tkinter.END))

  def DrawScreenNextStepButton(self, id_list, next_step_button_element, next_step_button_image_element):
    ui_imp_next_step_button = tkinter.Button(self.ui_imp_next_button_frame, text=next_step_button_element.GetText())
    self._ConfigureButtonImage(next_step_button_image_element, ui_imp_next_step_button)
    ui_imp_clickable = self._ConfigureButton(id_list, next_step_button_element, ui_imp_next_step_button)
    ui_imp_next_step_button.grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    return ParentElement(ui_imp_clickable)

  def DrawScreenPrevStepButton(self, id_list, prev_step_button_element, prev_step_button_image_element):
    ui_imp_prev_step_button = tkinter.Button(self.ui_imp_prev_button_frame, text=prev_step_button_element.GetText())
    self._ConfigureButtonImage(prev_step_button_image_element, ui_imp_prev_step_button)
    ui_imp_clickable = self._ConfigureButton(id_list, prev_step_button_element, ui_imp_prev_step_button)
    ui_imp_prev_step_button.grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    return ParentElement(ui_imp_clickable)

  def PrepareScreenMainButtonAndNavigationButtons(self, main_button=False, nav_button_num=0):
    if not (main_button or nav_button_num):
      return
    if main_button:
      total_button_num = math.ceil(nav_button_num / 2) * 2 + int(main_button)
      main_button_i = math.ceil(nav_button_num / 2)
    else:
      total_button_num = nav_button_num
      main_button_i = None

    ui_imp_footer_frame = tkinter.Frame(self.ui_imp_frame)
    ui_imp_footer_frame.grid(row=2, sticky=(tkinter.W, tkinter.E))
    self.ui_imp_main_button_frame = None
    self.ui_imp_nav_button_frame_list = []
    for button_i in range(total_button_num):
      if button_i == main_button_i:
        ui_imp_button_frame = tkinter.Frame(ui_imp_footer_frame, width=MAIN_BUTTON_WIDTH, height=MAIN_BUTTON_HEIGHT)
      else: 
        ui_imp_button_frame = tkinter.Frame(ui_imp_footer_frame, width=NAV_BUTTON_WIDTH, height=NAV_BUTTON_HEIGHT)
      ui_imp_button_frame.grid_propagate(False)
      ui_imp_button_frame.grid(column=button_i, row=0)
      ui_imp_button_frame.columnconfigure(0, weight=1)
      ui_imp_button_frame.rowconfigure(0, weight=1)
      ui_imp_footer_frame.columnconfigure(button_i, weight=1)
      if button_i == main_button_i:
        self.ui_imp_main_button_frame = ui_imp_button_frame
      else:
        self.ui_imp_nav_button_frame_list.append(ui_imp_button_frame)

  def DrawScreenMainButton(self, id_list, main_button_element, main_button_image_element):
    assert self.ui_imp_main_button_frame is not None
    ui_imp_main_button = tkinter.Button(self.ui_imp_main_button_frame, text=main_button_element.GetText())
    self._ConfigureButtonImage(main_button_image_element, ui_imp_main_button)
    ui_imp_main_button.grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

    if main_button_element.GetOnClick():
      ui_imp_main_button.configure(command=ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD))
      return ParentElement(ui_imp_main_button) 
    elif main_button_element.HasContextMenu():
      ui_imp_main_button_context_menu = tkinter.Menu()
      ui_imp_main_button.bind('<1>', lambda e: ui_imp_main_button_context_menu.post(e.x_root, e.y_root))
      return ParentElement(ui_imp_main_button_context_menu)
    else:
      return ParentElement(ui_imp_main_button)

  def DrawScreenNavButton(self, id_list, nav_button_element, nav_button_image_element, nav_button_i):
    assert nav_button_element.GetOnClick() is not None
    ui_imp_nav_button = tkinter.Button(
        self.ui_imp_nav_button_frame_list[nav_button_i],
        text=nav_button_element.GetText(), command=ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD))
    self._ConfigureButtonImage(nav_button_image_element, ui_imp_nav_button)
    ui_imp_nav_button.grid(sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))

  def _ConfigureParent(self, ui_imp_parent, maximize=False):
    if maximize:
      if ui_imp_parent.GetOrientation() == fase.Frame.VERTICAL:
        ui_imp_parent.GetUIImpParent().rowconfigure(ui_imp_parent.GetRow(), weight=1)
      elif ui_imp_parent.GetOrientation() == fase.Frame.HORIZONTAL:
        ui_imp_parent.GetUIImpParent().columnconfigure(ui_imp_parent.GetColumn(), weight=1)
      else:
        raise ValueError(self._orientation)

  def DrawRefreshButton(self, id_list, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_refresh_button = tkinter.Button(ui_imp_parent.GetUIImpParent(), text=REFRESH_BUTTON_TEXT)
    ui_imp_refresh_button.configure(command=ElementCallbackCallback(self, id_list, fase.ON_REFRESH_METHOD))
    ui_imp_refresh_button.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow())
    ui_imp_parent.Next()
    return ParentElement(ui_imp_refresh_button)

  def DrawFrame(self, id_list, frame_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent, maximize=(frame_element.GetSize()==fase.Frame.MAX))
    ui_imp_frame = tkinter.Frame(ui_imp_parent.GetUIImpParent())

    if frame_element.GetOrientation() == fase.Frame.VERTICAL:
      ui_imp_frame.columnconfigure(0, weight=1)
    elif frame_element.GetOrientation() == fase.Frame.HORIZONTAL:
      ui_imp_frame.rowconfigure(0, weight=1)
    else:
      raise ValueError(self._orientation)

    click_callback = None
    if frame_element.GetOnClick():
      click_callback = ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD)
    elif ui_imp_parent.GetClickCallback():
      click_callback = ui_imp_parent.GetClickCallback()

    if click_callback is not None:
      ui_imp_frame.bind('<1>', click_callback)

    if frame_element.GetBorder():
      ui_imp_frame.configure(borderwidth=1)
      ui_imp_frame.configure(relief='raised')

    if frame_element.GetDisplayed():
      ui_imp_frame.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                         sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_frame, orientation=frame_element.GetOrientation(), click_callback=click_callback)

  def DrawLabel(self, id_list, label_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent, maximize=(label_element.GetSize()==fase.Label.MAX))
    ui_imp_label = tkinter.Label(ui_imp_parent.GetUIImpParent(), text=label_element.GetText())

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
      click_callback = ElementCallbackCallback(self, id_list,fase.ON_CLICK_METHOD)
    elif ui_imp_parent.GetClickCallback():
      click_callback = ui_imp_parent.GetClickCallback()

    if click_callback is not None:
      ui_imp_label.bind('<1>', click_callback)

    if label_element.GetDisplayed():
      ui_imp_label.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                        sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_label)

  def DrawText(self, id_list, text_element, ui_imp_parent):
    if text_element.GetHint():
      self.DrawLabel(id_list, fase.Label(text=text_element.GetHint()), ui_imp_parent)
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = TextElementVariable(ui_imp_var)
    self.id_list_to_var[tuple(id_list)].Update(text_element.Get())
    ui_imp_var.trace('w', ElementUpdatedCallback(self, id_list))
    ui_imp_text = tkinter.Entry(ui_imp_parent.GetUIImpParent(), textvariable=ui_imp_var)
    if text_element.GetDisplayed():
      ui_imp_text.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                       sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_text)

  def DrawSwitch(self, id_list, switch_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = SwitchElementVariable(ui_imp_var)
    self.id_list_to_var[tuple(id_list)].Update(switch_element.Get())
    ui_imp_var.trace('w', ElementUpdatedCallback(self, id_list))
    ui_imp_switch = tkinter.Checkbutton(ui_imp_parent.GetUIImpParent(), text=switch_element.GetText(),
                                        variable=ui_imp_var, onvalue=str(True), offvalue=str(False))

    if switch_element.GetAlight() is not None:
      if switch_element.GetAlight() == fase.Switch.LEFT:
        anchor = 'w'
      elif switch_element.GetAlight() == fase.Switch.RIGHT:
        anchor = 'e'
      elif switch_element.GetAlight() == fase.Switch.CENTER:
        anchor = 'center'
      ui_imp_switch.configure(anchor=anchor)

    if switch_element.GetDisplayed():
      ui_imp_switch.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                         sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_switch)

  def DrawSelect(self, id_list, select_element, ui_imp_parent):
    if select_element.GetHint():
      self.DrawLabel(id_list, fase.Label(text=select_element.GetHint()), ui_imp_parent)
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = SelectElementVariable(ui_imp_var)
    self.id_list_to_var[tuple(id_list)].Update(select_element.Get())
    ui_imp_var.trace('w', ElementUpdatedCallback(self, id_list))
    ui_imp_select = tkinter.Spinbox(ui_imp_parent.GetUIImpParent(), values=select_element.GetItems(),
                                    textvariable=ui_imp_var)

    if select_element.GetAlight() is not None:
      if select_element.GetAlight() == fase.Switch.LEFT:
        anchor = 'w'
      elif select_element.GetAlight() == fase.Switch.RIGHT:
        anchor = 'e'
      elif select_element.GetAlight() == fase.Switch.CENTER:
        anchor = 'center'
      ui_imp_select.configure(anchor=anchor)

    if select_element.GetDisplayed():
      ui_imp_select.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                         sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_select)

  def DrawSlider(self, id_list, slider_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.DoubleVar()
    self.id_list_to_var[tuple(id_list)] = SliderElementVariable(ui_imp_var)
    self.id_list_to_var[tuple(id_list)].Update(slider_element.Get())
    ui_imp_var.trace('w', ElementUpdatedCallback(self, id_list))
    if ui_imp_parent.GetOrientation() == fase.Frame.VERTICAL:
      orient = 'horizontal'
    elif ui_imp_parent.GetOrientation() == fase.Frame.HORIZONTAL:
      orient = 'vertical'
    ui_imp_slider = tkinter.Scale(ui_imp_parent.GetUIImpParent(), from_=slider_element.GetMinValue(),
                                  to=slider_element.GetMaxValue(), orient=orient, variable=ui_imp_var)

    if slider_element.GetDisplayed():
      ui_imp_slider.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                         sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_slider)

  def DrawImage(self, id_list, image_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_photo = ImageTk.PhotoImage(Image.open(self.ui.GetResourceFilename(image_element.GetFilename())))
    ui_imp_image = tkinter.Label(ui_imp_parent.GetUIImpParent(), image=ui_imp_photo)
    ui_imp_image.image = ui_imp_photo
    if image_element.GetDisplayed(): 
      ui_imp_image.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow())
    ui_imp_parent.Next()
    return ParentElement(ui_imp_image) 

  def DrawButton(self, id_list, button_element, button_image_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_button = tkinter.Button(ui_imp_parent.GetUIImpParent(), text=button_element.GetText())
    self._ConfigureButtonImage(button_image_element, ui_imp_button)
    ui_imp_clickable = self._ConfigureButton(id_list, button_element, ui_imp_button)
    if button_element.GetDisplayed():
      ui_imp_button.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow())
    ui_imp_parent.Next()
    return ParentElement(ui_imp_clickable)

  def DrawContactPicker(self, id_list, contact_picker_element, ui_imp_parent):
    if contact_picker_element.GetHint():
      self.DrawLabel(id_list, fase.Label(text=contact_picker_element.GetHint()), ui_imp_parent)
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = ContactPickerElementVariable(ui_imp_var)
    self.id_list_to_var[tuple(id_list)].Update(contact_picker_element.Get())
    ui_imp_text = tkinter.Entry(ui_imp_parent.GetUIImpParent(), textvariable=ui_imp_var)

    if contact_picker_element.GetOnPick():
      ui_imp_text.bind('<FocusOut>', ElementUpdatedAndCallbackCallback(self, id_list, fase.ON_PICK_METHOD))
    else:
      ui_imp_text.bind('<FocusOut>', ElementUpdatedCallback(self, id_list))

    if contact_picker_element.GetDisplayed():
      ui_imp_text.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                       sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_text)

  def DrawDateTimePicker(self, id_list, datetime_picker_element, ui_imp_parent):
    if datetime_picker_element.GetHint():
      self.DrawLabel(id_list, fase.Label(text=datetime_picker_element.GetHint()), ui_imp_parent)
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = (
        DateTimePickerElementVariable(ui_imp_var, type_=datetime_picker_element.GetType()))
    self.id_list_to_var[tuple(id_list)].Update(datetime_picker_element.Get())
    ui_imp_text = tkinter.Entry(ui_imp_parent.GetUIImpParent(), textvariable=ui_imp_var)
    ui_imp_text.bind('<FocusOut>', ElementUpdatedCallback(self, id_list))

    if datetime_picker_element.GetDisplayed():
      ui_imp_text.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                       sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_text)

  def DrawPlacePicker(self, id_list, place_picker_element, ui_imp_parent):
    if place_picker_element.GetHint():
      self.DrawLabel(id_list, fase.Label(text=place_picker_element.GetHint()), ui_imp_parent)
    self._ConfigureParent(ui_imp_parent)
    ui_imp_var = tkinter.StringVar()
    self.id_list_to_var[tuple(id_list)] = PlacePickerElementVariable(ui_imp_var, type_=place_picker_element.GetType())
    self.id_list_to_var[tuple(id_list)].Update(place_picker_element.Get())
    ui_imp_text = tkinter.Entry(ui_imp_parent.GetUIImpParent(), textvariable=ui_imp_var)
    ui_imp_text.bind('<FocusOut>', ElementUpdatedCallback(self, id_list))
    
    if place_picker_element.GetDisplayed():
      ui_imp_text.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                       sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_text)

  def DrawSeparator(self, id_list, separator_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    if ui_imp_parent.GetOrientation() == fase.Frame.VERTICAL:
      orient = 'horizontal'
    elif ui_imp_parent.GetOrientation() == fase.Frame.HORIZONTAL:
      orient = 'vertical'
    ui_imp_separator = ttk.Separator(ui_imp_parent.GetUIImpParent(), orient=orient)

    if separator_element.GetDisplayed():
      ui_imp_separator.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                            sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_separator)

  def DrawWeb(self, id_list, web_element, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent, maximize=(web_element.GetSize()==fase.Web.MAX))
    ui_imp_web = tkinter.Label(ui_imp_parent.GetUIImpParent(), text=web_element.GetUrl())

    if web_element.GetDisplayed():
      ui_imp_web.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow(),
                      sticky=(tkinter.S, tkinter.N, tkinter.E, tkinter.W))
    ui_imp_parent.Next()
    return ParentElement(ui_imp_web)

  def DrawContextMenuItem(self, id_list, menu_item_element, menu_item_image_element, ui_imp_parent):
    assert menu_item_element.GetOnClick() is not None
    ui_imp_menu = ui_imp_parent.GetUIImpParent() 
    ui_imp_menu.add_command(
        label=menu_item_element.GetText(), command=ElementCallbackCallback(self, id_list, fase.ON_CLICK_METHOD))
    self._ConfigureMenuItemImage(menu_item_image_element, ui_imp_menu, ui_imp_menu.index(tkinter.END))

  def DrawMoreButton(self, id_list, ui_imp_parent):
    self._ConfigureParent(ui_imp_parent)
    ui_imp_more_button = tkinter.Button(ui_imp_parent.GetUIImpParent(), text=ON_MORE_BUTTON_TEXT)
    ui_imp_more_button.configure(command=ElementCallbackCallback(self, id_list, fase.ON_MORE_METHOD))
    ui_imp_more_button.grid(column=ui_imp_parent.GetColumn(), row=ui_imp_parent.GetRow())
    ui_imp_parent.Next()
    return ParentElement(ui_imp_more_button)

  # NOTE(igushev): tkinter has limitation on what dialog boxes can be displayed.
  def ShowAlert(self, alert, button_text_tuple):
    return messagebox.showinfo(type=BUTTON_TEXT_LIST_TO_INFO_TYPE[button_text_tuple], message=alert.GetText())

  def Run(self):
    self.ui_imp_root.after(SCREEN_UPDATE_INTERVAL, self.ScreenUpdate)
    self.ui_imp_root.mainloop()

  def ElementUpdated(self, id_list):
    if self.element_updated_callback:
      value = self.id_list_to_var[tuple(id_list)].Get() 
      self.ui.ElementUpdated(id_list, value)

  def ScreenUpdate(self):
    self.ui.ScreenUpdate()
    self.ui_imp_root.after(SCREEN_UPDATE_INTERVAL, self.ScreenUpdate)

  def ElementCallback(self, id_list, method):
    self.ui.ElementCallback(id_list, method)

  def ElementUpdatedReceived(self, id_list, value):
    # NOTE(igushev): We turn off element_updated_callback not to register change as user's change.
    self.element_updated_callback = False
    self.id_list_to_var[tuple(id_list)].Update(value)
    self.element_updated_callback = True
