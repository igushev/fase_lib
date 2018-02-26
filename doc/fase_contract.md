Table of Contents
=================
   * [Communication with Server](#communication-with-server)
      * [Data Classes](#data-classes)
      * [Client](#client)
         * [Client Launch](#client-launch)
         * [Keeping Dictionary of Updated Elements](#keeping-dictionary-of-updated-elements)
         * [Keeping Dictionary of Elements](#keeping-dictionary-of-elements)
         * [Updating Server](#updating-server)
         * [Element Callback](#element-callback)
         * [Processing Response](#processing-response)
   * [Fase Elements](#fase-elements)
      * [Comparing Fase Elements to similar Elements in iOS/Android/Tkinter](#comparing-fase-elements-to-similar-elements-in-iosandroidtkinter)
      * [Data Classes](#data-classes-1)
      * [Elements Classes](#elements-classes)
   * [Mobile Device Specifics](#mobile-device-specifics)
   * [Fase Application Examples](#fase-application-examples)
      * [Hello World Application](#hello-world-application)
         * [Initial Screen](#initial-screen)
         * [Hello Screen](#hello-screen)

# Communication with Server
## Data Classes
* **Device**
  * *device_type*: string
  * *device_token*: string

* **SessionInfo**
  * *session_id*: string

* **ScreenInfo**
  * *screen_id*: string

* **ElementsUpdate**
  * *id_list_list*: list(list(string))
  * *value_list*: list(string)

* **ScreenUpdate**
  * *elements_update*: *ElementsUpdate*
  * *device*: *Device*

* **ElementCallback**
  * *elements_update*: *ElementsUpdate*
  * *id_list*: list(string)
  * *method*: string
  * *locale*: *Locale*
  * *device*: *Device*

* **Response**
  * *elements_update*: *ElementsUpdate*
  * *screen_info*: *ScreenInfo*
  * *session_info*: *SessionInfo*
  * *screen*: *Screen* or subclass

* **Command**
  * *command*: string

* **Status**
  * *message*: string

* **BadRequest**
  * *code*: int
  * *message*: string

## Client

### Client Launch

When Client launches first time, it sends */getserivce* request to Server, receives and processes *Response*. When
Client launches second and following times, it reads previously saved **locally** session_info, sends */getscreen*
request to Server, receives and processes *Response*.

### Keeping Dictionary of Updated Elements

Client maintains internal dictionary *list(id)* to *str*, where *list(id)* is list of ids to traverse Element
Tree and *str* is serialized value of the *Element* (refer to each type of *Element* description). The dictionary is
empty when Client draws the *Screen*. When User interacts with an *Element*, internal dictionary is appended or updated.

### Keeping Dictionary of Elements

It make sense to keep dictionary *list(id)* to *Element* as well when Client draws the *Screen*. It'll help to process *Response*, when *ElementUpdate* is received (read below).

### Updating Server

Client sends each 200ms (configurable) */screenupdate* request with *ScreenUpdate* message, where it has content of the
dictionary and device token, receives and processes *Response*. This update happens **asynchronous** meaning
non-blocking for User.

If update hasn't finished for previous iteration, next one can be skip. This might be controlled by *condition*
synchronization primitive (refer to Client's language).

The dictionary is refreshed each time */screenupdate* request is sent and data is collected from dictionary to form *ScreenUpdate* message.

Example of *ScreenUpdate* message for Hello World Application when User enters his/her name:
```
{ 'device': { 'device_token': 'ec868e22-b79f-4bf9-8783-c9e6be940dcf',
              'device_type': 'Python'},
  'elements_update': { 'id_list_list': [['text_name_id']],
                       'value_list': ['Edward']}}
```

### Element Callback

When User interacts with *Screen* and triggers callback (Button click, Screen Refresh, Picking Contact), Client sends
*/elementcallback* request with *ElementCallback* message, where it has content of the dictionary, *list(id)* of the
*Element* which caused callback, name of the callback method and device token, receives and processes *Response*.
Callback processing happens **synchronous** meaning blocking for User.

Additional data can be requested for the callback, for example, current *Locale*. If So, Client using its platform API
obtains such information and sends within message.

Example of *ElementCallback* message for Hello World Application when User clicks "Next" button:
```
{ 'device': { 'device_token': '10a69d1a-93d1-4063-8494-894efc412228',
              'device_type': 'Python'},
  'elements_update': None,
  'id_list': ['next_button_id'],
  'locale': None,
  'method': 'on_click'}
```

### Processing Response

* If received *Screen* has Alert, it is shown to user in blocking fashion and Client instantly sends */elementcallback*
requests with information about user's choice in same format;
* Client saves **locally** current session_id and screen_id;
* If new *Screen* is received, Client draws new *Screen*;
* If *ElementUpdate* is received, Client updates the Elements.

Example of *Response* message for Hello World Application when User clicks "Next" button:
```
{ 'elements_update': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase',
              '_screen_id': 'be22837e30feaed208e70d01911a5630',
              'displayed': True,
              'id_element_list': [ [ 'hello_label_id',
                                     { '__class__': 'Label',
                                       '__module__': 'fase',
                                       'alight': None,
                                       'displayed': True,
                                       'font': None,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': None,
                                       'request_locale': False,
                                       'size': None,
                                       'text': 'Hello, Edward!'}],
                                   [ 'reset_button_id',
                                     { '__class__': 'Button',
                                       '__module__': 'fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'image': None,
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase'},
                                       'request_locale': False,
                                       'text': 'Reset'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': 'be22837e30feaed208e70d01911a5630'},
  'session_info': {'session_id': '0ca8467a8bf9f9ec4e862721af6f592b'}}
```

# Fase Elements
## Comparing Fase Elements to similar Elements in iOS/Android/Tkinter
|Fase|iOS|Android|Tkinter|
|----|---|-------|-------|
|Frame|UIView|FrameLayout|Frame|
|Label|UILabel|TextView|Label|
|Text|UITextField|EditText|Entry|
|Switch|UISwitch|Switch|CheckButton|
|Select|UIPickerView|Spinners|ComboBox|
|Slider|UISlider|SeekBar|Scale|
|Image|UIImage|ImageView|Label|
|MenuItem|||Menu.add_command|
|Menu|||Menu|
|Button|UIButton|Button|Button|
|ButtonBar|||-|
|ContactPicker|||-|
|DateTimePicker|UIDatePicker|DatePicker|-|
|PlacePicker|Implemented using Google Place Picker|Implemented using Google Place Picker|-|
|Separator|-|-|Separator|
|Web|WKWebView|WebView|-|

## Data Classes
* **Locale**
  * *country_code*: string

* **Contact**
  * *display_name*: string
  * *phone_number*: string

* **Place**
  * *google_place_id*: string
  * *country*: string
  * *state*: string
  * *city*: string

* **User**
  * *date_of_birth*: date
  * *last_name*: string
  * *home_city*: *Place*
  * *phone_number*: string
  * *first_name*: string
  * *datetime_added*: date
  * *user_id*: string

## Elements Classes
* **Element**. Basic Interface.

* **ElementContainer** extends *Element*. Basic Interface which contains list if id and Element pairs.
  * *id_element_list*: list(tuple(string, *Element* or subclass))

* **VisualElement** extends *ElementContainer*. Basic Interface for Visual Elements.
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *displayed*: bool. If the Element should be displayed on the Screen.
  * *locale*: *Locale*. Ignore.
  * *request_locale*: bool. If the Element requests current Local during a Callback. 

* **Label** extends *VisualElement*
  * *on_click*: function
  * *alight*: int
    * LEFT = 1
    * RIGHT = 2
    * CENTER = 3
  * *font*: float
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *size*: int
    * MIN = 1
    * MAX = 2
  * *text*: string
  * *displayed*: bool
  * *request_locale*: bool

* **Text** extends *VisualElement*
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *size*: int
    * MIN = 1
    * MAX = 2
  * *text*: string
  * *displayed*: bool
  * *request_locale*: bool
  * *hint*: string

* **Switch** extends *VisualElement*
  * *displayed*: bool
  * *alight*: int
    * LEFT = 1
    * RIGHT = 2
    * CENTER = 3
  * *request_locale*: bool
  * *text*: string
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *value*: bool
  * *locale*: *Locale*

* **Select** extends *VisualElement*
  * *items*: list(string)
  * *alight*: int
    * LEFT = 1
    * RIGHT = 2
    * CENTER = 3
  * *value*: string
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *displayed*: bool
  * *request_locale*: bool
  * *hint*: string

* **Image** extends *VisualElement*
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *image*: string
  * *displayed*: bool
  * *request_locale*: bool

* **MenuItem** extends *VisualElement*
  * *on_click*: function
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *image*: string
  * *request_locale*: bool
  * *text*: string
  * *displayed*: bool
  * *locale*: *Locale*

* **Menu** extends *ElementContainer*
  * *text*: string
  * *id_element_list*: list(tuple(string, *Element* or subclass))

* **Button** extends *VisualElement*
  * *on_click*: function
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *image*: string
  * *request_locale*: bool
  * *text*: string
  * *displayed*: bool
  * *locale*: *Locale*

* **ButtonBar** extends *ElementContainer*
  * *id_element_list*: list(tuple(string, *Element* or subclass))

* **ContactPicker** extends *VisualElement*
  * *request_locale*: bool
  * *contact*: *Contact*
  * *on_pick*: function
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *size*: int
    * MIN = 1
    * MAX = 2
  * *displayed*: bool
  * *hint*: string

* **DateTimePicker** extends *VisualElement*
  * *request_locale*: bool
  * *datetime*: date
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *size*: int
    * MIN = 1
    * MAX = 2
  * *type*: int
    * DATE = 1
    * TIME = 2
    * DATETIME = 3
  * *displayed*: bool
  * *hint*: string

* **PlacePicker** extends *VisualElement*
  * *request_locale*: bool
  * *place*: *Place*
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *size*: int
    * MIN = 1
    * MAX = 2
  * *type*: int
    * CITY = 1
  * *displayed*: bool
  * *hint*: string

* **BaseElementsContainer** extends *VisualElement*
  * *displayed*: bool
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *locale*: *Locale*
  * *request_locale*: bool

* **Frame** extends *BaseElementsContainer*
  * *on_click*: function
  * *orientation*: int
    * VERTICAL = 1
    * HORIZONTAL = 2
  * *border*: bool
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *size*: int
    * MIN = 1
    * MAX = 2
  * *displayed*: bool
  * *request_locale*: bool

* **Alert** extends *ElementContainer*
  * *text*: string
  * *id_element_list*: list(tuple(string, *Element* or subclass))

* **Screen** extends *BaseElementsContainer*
  * *on_refresh*: function
  * *request_locale*: bool
  * *title*: string
  * *_screen_id*: string
  * *locale*: *Locale*
  * *id_element_list*: list(tuple(string, *Element* or subclass))
  * *scrollable*: bool
  * *displayed*: bool
  * *on_more*: function

*Screen* can have one or following Elements:

|id|Element|Description|
|--|-------|-----------|
|'next_step_button'|Button|Button responsible for Next step ("Save", "Done", "Send")|
|'prev_step_button'|Button|Button responsible for Previous step ("Cancel", "Back")|
|'context_menu'|Menu|Screen context menu which is usually accessible via button in right upper corner|
|'alert'|Alert|Information needed to show Alert|
|'main_menu'|Menu|Main Menu, usually big menu accessible via button on left upper corner| 
'main_button'|Button|Main Button responsible for main action ("New"), usually bigger than other navigation buttons. On iOS usually in the middle of bottom navigation bar, on Android usually separate Button on right lower corner|
|'button_bar'|Button Bar|Collection of navigation buttons. On iOS usually are bottom buttons, on Android usually located in Main Menu|

# Mobile Device Specifics
|Element|iOS|Android|Windows Phone|
|-------|---|-------|-------------|
|Button bar|Bottom|In main menu|Top and Bottom|
|Main button|Big button in the middle of the button bar|Big button in the right bottom corner|Button in the middle of the button bar|
|Main menu|Main menu from left top button|Main menu from left top button, item below button bar items|Main menu from left top button|
|Context menu|Right top corner|Right top corner|Right bottom corner|

# Fase Application Examples

## Hello World Application

### Initial Screen
Initial Screen has only Text field for entering name and "Next" button.

**JSON**
```
{ '__class__': 'Screen',
  '__module__': 'fase',
  '_screen_id': '9c7d046753f21a6b4bc393a4e8615578',
  'displayed': True,
  'id_element_list': [ [ 'text_name_id',
                         { '__class__': 'Text',
                           '__module__': 'fase',
                           'displayed': True,
                           'hint': 'Enter Name',
                           'id_element_list': [],
                           'locale': None,
                           'request_locale': False,
                           'size': None,
                           'text': None}],
                       [ 'next_button_id',
                         { '__class__': 'Button',
                           '__module__': 'fase',
                           'displayed': True,
                           'id_element_list': [],
                           'image': None,
                           'locale': None,
                           'on_click': { '__func__': 'FunctionPlaceholder',
                                         '__module__': 'fase'},
                           'request_locale': False,
                           'text': 'Next'}]],
  'locale': None,
  'on_more': None,
  'on_refresh': None,
  'request_locale': False,
  'scrollable': None,
  'title': None}
```
**Screenshot**
![Initial Screen](hello_world_screenshots/initial_screen.png "Initial Screen")

### Hello Screen
After clicking on "Next" button, Hello Screen has greeting and "Reset" button. "Reset" button returns application to
Initial Screen.
 
**JSON**
```
{ '__class__': 'Screen',
  '__module__': 'fase',
  '_screen_id': '16aecadcddb108840fcb39bb8e667f6e',
  'displayed': True,
  'id_element_list': [ [ 'hello_label_id',
                         { '__class__': 'Label',
                           '__module__': 'fase',
                           'alight': None,
                           'displayed': True,
                           'font': None,
                           'id_element_list': [],
                           'locale': None,
                           'on_click': None,
                           'request_locale': False,
                           'size': None,
                           'text': 'Hello, Edward!'}],
                       [ 'reset_button_id',
                         { '__class__': 'Button',
                           '__module__': 'fase',
                           'displayed': True,
                           'id_element_list': [],
                           'image': None,
                           'locale': None,
                           'on_click': { '__func__': 'FunctionPlaceholder',
                                         '__module__': 'fase'},
                           'request_locale': False,
                           'text': 'Reset'}]],
  'locale': None,
  'on_more': None,
  'on_refresh': None,
  'request_locale': False,
  'scrollable': None,
  'title': None}
```
**Screenshot**
![Hello Screen](hello_world_screenshots/hello_screen.png "Hello Screen")

