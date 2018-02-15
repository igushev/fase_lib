# Communication with Server
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

