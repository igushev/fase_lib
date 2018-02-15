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

When Client launches first time, it sends */getserivce* request to Server, receives and processes *Response*. When Client launches second and following times, it reads previously saved **locally** session_info, sends */getscreen* request to
Server, receives and processes *Response*.

### Keeping Dictionary of Updated Elements

Client maintains internal dictionary *list(id)* to *str*, where *list(id)* is list of ids to traverse Element
Tree and *str* is serialized value of the Element. The dictionary is empty when Client draws the *Screen*. When User
interacts with an Element, internal dictionary is updated.

### Keeping Dictionary of Elements

It make sense to keep dictionary *list(id)* to *Element* as well when Client draws the *Screen*. It'll help to process *Response*, when *ElementUpdate* is received (read below).

### Updating Server

Client sends each 200ms (configurable) */screenupdate* request with *ScreenUpdate* message, where it has content of the
dictionary and device token, receives and processes *Response*. This update happens **asynchronous** meaning
non-blocking for User.

If update hasn't finished for previous iteration, next one can be skip. This might be controlled by *condition*
synchronization primitive.

The dictionary isn't refreshed each time */screenupdate* request is sent, instead it keeps state since Client draws the
*Screen*. 

### Element Callback

When User interacts with *Screen* and triggers callback (Button click, Screen Refresh, Picking Contact), Client sends
*/elementcallback* request with *ElementCallback* message, where it has content of the dictionary, *list(id)* of the
element which caused callback, name of the callback method and device token, receives and processes *Response*. Callback
processing happens **synchronous** meaning blocking for User.

### Processing Response

* If received *Screen* has Alert, it is shown to user in blocking fashion and Client instantly sends */elementcallback*
requests with information about user's choice in same format.
* Client saves current session_id and screen_id
* If new *Screen* is received, Client draws new *Screen*.
* If *ElementUpdate* is received, Client updates the Elements.
    