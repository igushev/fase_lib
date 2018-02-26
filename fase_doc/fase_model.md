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
