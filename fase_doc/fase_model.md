Table of Contents
=================

   * [Communication with Server](#communication-with-server)
      * [Data Classes](#data-classes)
      * [Server API](#server-api)
      * [Client](#client)
         * [Client Launch](#client-launch)
         * [Keeping Dictionary of Updated Elements](#keeping-dictionary-of-updated-elements)
         * [Keeping Dictionary of Elements](#keeping-dictionary-of-elements)
         * [Updating Server](#updating-server)
         * [Element Callback](#element-callback)
         * [Processing Response](#processing-response)
   * [Fase Application Examples](#fase-application-examples)
      * [Hello World Application. Slow User](#hello-world-application-slow-user)
         * [Client Starts](#client-starts)
         * [User Types Name](#user-types-name)
         * [User Clicks Next](#user-clicks-next)
         * [Hello Screen](#hello-screen)
         * [User Clicks Reset](#user-clicks-reset)
      * [Hello World Application. Quick User](#hello-world-application-quick-user)
         * [Client Starts](#client-starts-1)
         * [User Types Name and Clicks Next](#user-types-name-and-clicks-next)
      * [Hello World Application. External Data](#hello-world-application-external-data)
         * [Client Starts](#client-starts-2)
         * [Name Received](#name-received)

# Communication with Server
## Data Classes
* **SessionInfo**
  * *session_id*: string

* **ScreenInfo**
  * *screen_id*: string

* **Device**
  * *device_type*: string
  * *device_token*: string

* **Resource**
  * *filename*: string

* **Resources**
  * *resource_list*: list(*Resource*)

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
  * *device*: *Device*
  * *locale*: *Locale*

* **ScreenProg**
  * *session_id*: string
  * *screen*: *Screen* or subclass
  * *elements_update*: *ElementsUpdate*
  * *recent_device*: *Device*

* **Response**
  * *screen*: *Screen* or subclass
  * *resources*: *Resources*
  * *elements_update*: *ElementsUpdate*
  * *session_info*: *SessionInfo*
  * *screen_info*: *ScreenInfo*

* **Command**
  * *command*: string

* **Status**
  * *message*: string

* **BadRequest**
  * *code*: int
  * *message*: string

## Server API
|HTTP Request|HTTP Method|Need session_id|Need screen_id|Input Type|Output Type|Description|
|------------|-----------|---------------|--------------|----------|-----------|-----------|
|/sendinternalcommand|'POST', 'OPTIONS'||||Command|Status|Internal command to the framework|
|/sendservicecommand|'POST', 'OPTIONS'|||Command|Status|Internal command to Service|
|/getservice|'POST', 'OPTIONS'|||Device|Response|Create instance of the Service|
|/getscreen|'POST', 'OPTIONS'|Yes||Device|Response|Get current Screen|
|/screenupdate|'POST', 'OPTIONS'|Yes|Yes|ScreenUpdate|Response|Send information about current field state|
|/elementcallback|'POST', 'OPTIONS'|Yes|Yes|ElementCallback|Response|Send information about registered callback|
|/getresource/filename/ <path:filename>|'GET', 'OPTIONS'||||<File>|Request resource by filename|

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
* Every *Response* might have *Resources* field which has list of *Resource* objects. Currently *Resource* might contain
only filename of given resource. If *Resources* is present, Client must request all missing locally resources in
**parallel** and save them **locally**. Filename serves as unique id of given resource.

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

# Fase Application Examples

## Hello World Application. Slow User

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
{ 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
  'device_type': 'Python'}
```
Server sends *Response* with initial *Screen*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase.fase',
              '_screen_id': '7c2cfa33c307697c560ec0683565f248',
              'displayed': True,
              'id_element_list': [ [ 'text_name_id',
                                     { '__class__': 'Text',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'hint': 'Enter Name',
                                       'id_element_list': [],
                                       'locale': None,
                                       'request_locale': False,
                                       'size': None,
                                       'text': None,
                                       'type': None}],
                                   [ 'next_button_id',
                                     { '__class__': 'Button',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase.fase'},
                                       'request_locale': False,
                                       'text': 'Next'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### User Types Name
Client keeps sending `/screenupdate` with *ScreenUpdate*

When user hasn't typed anything:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server sends *Response*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User typed 'Ed':
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': {'id_list_list': [['text_name_id']], 'value_list': ['Ed']}}
```
Server sends *Response*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User stoped typing, text field still has 'Ed':
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server sends *Response*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User added 'ward' and finished typing 'Edward':
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': { 'id_list_list': [['text_name_id']],
                       'value_list': ['Edward']}}
```
Server sends *Response*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User hasn't been typing but text field still has 'Edward':
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server sends *Response*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### User Clicks Next
**If User clicks Next before Server sends ScreenUpdate with typed name, elements_update field would not be empty
(look Quick User case)!**
Client sends `/elementcallback` with *ElementCallback*:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None,
  'id_list': ['next_button_id'],
  'locale': None,
  'method': 'on_click'}
```
Server sends *Response* with new *Screen*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase.fase',
              '_screen_id': '20d0a7775a1ab89639aa2d91e3bbf862',
              'displayed': True,
              'id_element_list': [ [ 'hello_label_id',
                                     { '__class__': 'Label',
                                       '__module__': 'fase.fase',
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
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase.fase'},
                                       'request_locale': False,
                                       'text': 'Reset'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': '20d0a7775a1ab89639aa2d91e3bbf862'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### Hello Screen
Client keeps sending `/screenupdate` with *ScreenUpdate*, but they're empty since no text fields are present:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server sends *Response*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '20d0a7775a1ab89639aa2d91e3bbf862'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### User Clicks Reset
User clicks on 'Reset' button, client sends `/elementcallback` with *ElementCallback*:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None,
  'id_list': ['reset_button_id'],
  'locale': None,
  'method': 'on_click'}
```
Server sends *Response* with initial *Screen*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase.fase',
              '_screen_id': '5e0f5a04869b789295d911ed51373619',
              'displayed': True,
              'id_element_list': [ [ 'text_name_id',
                                     { '__class__': 'Text',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'hint': 'Enter Name',
                                       'id_element_list': [],
                                       'locale': None,
                                       'request_locale': False,
                                       'size': None,
                                       'text': None,
                                       'type': None}],
                                   [ 'next_button_id',
                                     { '__class__': 'Button',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase.fase'},
                                       'request_locale': False,
                                       'text': 'Next'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': '5e0f5a04869b789295d911ed51373619'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

## Hello World Application. Quick User

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
{ 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
  'device_type': 'Python'}
```
Server sends *Response* with initial *Screen*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase.fase',
              '_screen_id': '7c2cfa33c307697c560ec0683565f248',
              'displayed': True,
              'id_element_list': [ [ 'text_name_id',
                                     { '__class__': 'Text',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'hint': 'Enter Name',
                                       'id_element_list': [],
                                       'locale': None,
                                       'request_locale': False,
                                       'size': None,
                                       'text': None,
                                       'type': None}],
                                   [ 'next_button_id',
                                     { '__class__': 'Button',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase.fase'},
                                       'request_locale': False,
                                       'text': 'Next'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### User Types Name and Clicks Next
User is very quick, types the name and clicks Next. Client sends `/elementcallback` with *ElementCallback* with
*elements_update* field with just entered information:
```
{ 'device': { 'device_token': '885cb625-875b-41ec-8010-61d2a0e70d81',
              'device_type': 'Python'},
  'elements_update': { 'id_list_list': [['text_name_id']],
                       'value_list': ['Edward']},
  'id_list': ['next_button_id'],
  'locale': None,
  'method': 'on_click'}
```
Server sends *Response* with new *Screen*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase.fase',
              '_screen_id': 'ef8bf7814e513e541fad33ee1cc2e9f8',
              'displayed': True,
              'id_element_list': [ [ 'hello_label_id',
                                     { '__class__': 'Label',
                                       '__module__': 'fase.fase',
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
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase.fase'},
                                       'request_locale': False,
                                       'text': 'Reset'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': 'ef8bf7814e513e541fad33ee1cc2e9f8'},
  'session_info': {'session_id': 'ed014cd4fa322ebd98072811b7806229'}}
```

## Hello World Application. External Data

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
{ 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
  'device_type': 'Python'}
```
Server sends *Response* with initial *Screen*:
```
{ 'elements_update': None,
  'resources': None,
  'screen': { '__class__': 'Screen',
              '__module__': 'fase.fase',
              '_screen_id': '7c2cfa33c307697c560ec0683565f248',
              'displayed': True,
              'id_element_list': [ [ 'text_name_id',
                                     { '__class__': 'Text',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'hint': 'Enter Name',
                                       'id_element_list': [],
                                       'locale': None,
                                       'request_locale': False,
                                       'size': None,
                                       'text': None,
                                       'type': None}],
                                   [ 'next_button_id',
                                     { '__class__': 'Button',
                                       '__module__': 'fase.fase',
                                       'displayed': True,
                                       'id_element_list': [],
                                       'locale': None,
                                       'on_click': { '__func__': 'FunctionPlaceholder',
                                                     '__module__': 'fase.fase'},
                                       'request_locale': False,
                                       'text': 'Next'}]],
              'locale': None,
              'on_more': None,
              'on_refresh': None,
              'request_locale': False,
              'scrollable': None,
              'title': None},
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### Name Received
Client keeps sending `/screenupdate` with *ScreenUpdate*

When user hasn't typed anything:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server sends *Response* with *elements_update* field 
```
{ 'elements_update': { 'id_list_list': [['text_name_id']],
                       'value_list': ['John']},
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
**Client fills text field with 'John'!**
