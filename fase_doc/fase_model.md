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
      * [Hello World Application. Screen Update Examples](#hello-world-application-screen-update-examples)
         * [Client Starts](#client-starts)
         * [User Types Name](#user-types-name)
         * [User Clicks Next](#user-clicks-next)
         * [Hello Screen](#hello-screen)
         * [User Clicks Reset](#user-clicks-reset)
      * [Hello World Application. Element Callback Examples](#hello-world-application-element-callback-examples)
         * [Client Starts](#client-starts-1)
         * [User Types Name and Clicks Next](#user-types-name-and-clicks-next)
      * [Hello World Application. External Data Examples](#hello-world-application-external-data-examples)
         * [Client Starts](#client-starts-2)
         * [Name Received](#name-received)
      * [Notes Application. Resources Management Examples. Signing Up](#notes-application-resources-management-examples-signing-up)
         * [Client Starts](#client-starts-3)
         * [User Click Sign In on Dashboard Screen](#user-click-sign-in-on-dashboard-screen)
         * [User Clicks Sign Up on Sign In/Sign Up Screen](#user-clicks-sign-up-on-sign-insign-up-screen)
         * [User Enters Information and Clicks Sign Up](#user-enters-information-and-clicks-sign-up)
         * [User Enters Activation Code and Clicks Send](#user-enters-activation-code-and-clicks-send)
      * [Notes Application. Resources Management Examples. Adding New Note](#notes-application-resources-management-examples-adding-new-note)
         * [Client Starts](#client-starts-4)
         * [User Click Main Button](#user-click-main-button)
         * [User Enters Data and Clicks Next Button](#user-enters-data-and-clicks-next-button)

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
**Please note that session-id and screen-id have "-"! It's relevant only in HTTP headers, in other places they have "_"!**
|HTTP Request|HTTP Method|Need session-id|Need screen-id|Input Type|Output Type|Description|
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

# Fase Application Examples

## Hello World Application. Screen Update Examples

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
method: post
request: /getservice
```
```
{
  "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
  "device_type": "Python"
}
```
Server sends *Response* with Initial *Screen*:
```
{
  "screen": {
    "on_refresh": null,
    "id_element_list": [
      [
        "text_name_id",
        {
          "id_element_list": [],
          "displayed": true,
          "request_locale": false,
          "__module__": "fase.fase",
          "__class__": "Text",
          "type": null,
          "text": null,
          "multiline": null,
          "locale": null,
          "size": null,
          "hint": "Enter Name"
        }
      ],
      [
        "next_button_id",
        {
          "id_element_list": [],
          "displayed": true,
          "request_locale": false,
          "__module__": "fase.fase",
          "__class__": "Button",
          "text": "Next",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "locale": null
        }
      ]
    ],
    "displayed": true,
    "request_locale": false,
    "title": null,
    "__class__": "Screen",
    "_screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d",
    "__module__": "fase.fase",
    "scrollable": null,
    "on_more": null,
    "locale": null
  },
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d"
  }
}
```

### User Types Name
Client keeps sending `/screenupdate` with *ScreenUpdate*

When user hasn't typed anything:
```
method: post
request: /screenupdate
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': '01e5fb37f49192d3d34fe9e6c5e1932d'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "elements_update": null
}
```
Server sends *Response*:
```
{
  "screen": null,
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d"
  }
}
```
User typed 'Ed':
```
method: post
request: /screenupdate
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': '01e5fb37f49192d3d34fe9e6c5e1932d'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "elements_update": {
    "id_list_list": [
      [
        "text_name_id"
      ]
    ],
    "value_list": [
      "Ed"
    ]
  }
}
```
Server sends *Response*:
```
{
  "screen": null,
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d"
  }
}

```
User stoped typing, text field still has 'Ed':
```
method: post
request: /screenupdate
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': '01e5fb37f49192d3d34fe9e6c5e1932d'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "elements_update": null
}
```
Server sends *Response*:
```
{
  "screen": null,
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d"
  }
}
```
User added 'ward' and finished typing 'Edward' (entire context of the text field):
```
method: post
request: /screenupdate
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': '01e5fb37f49192d3d34fe9e6c5e1932d'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "elements_update": {
    "id_list_list": [
      [
        "text_name_id"
      ]
    ],
    "value_list": [
      "Edward"
    ]
  }
}
```
Server sends *Response*:
```
{
  "screen": null,
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d"
  }
}
```
User hasn't been typing but text field still has 'Edward':
```
method: post
request: /screenupdate
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': '01e5fb37f49192d3d34fe9e6c5e1932d'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "elements_update": null
}
```
Server sends *Response*:
```
{
  "screen": null,
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "01e5fb37f49192d3d34fe9e6c5e1932d"
  }
}

```

### User Clicks Next
**If User clicks Next before Server sends ScreenUpdate with typed name, elements_update field would not be empty
(look Quick User case)!**

Client sends `/elementcallback` with *ElementCallback*:
```
method: post
request: /elementcallback
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': '01e5fb37f49192d3d34fe9e6c5e1932d'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "method": "on_click",
  "elements_update": null,
  "id_list": [
    "next_button_id"
  ],
  "locale": null
}

```
Server sends *Response* with Greeting *Screen*:
```
{
  "screen": {
    "on_refresh": null,
    "id_element_list": [
      [
        "hello_label_id",
        {
          "id_element_list": [],
          "displayed": true,
          "request_locale": false,
          "__module__": "fase.fase",
          "font": null,
          "__class__": "Label",
          "text": "Hello, Edward!",
          "alight": null,
          "on_click": null,
          "size": null,
          "locale": null
        }
      ],
      [
        "reset_button_id",
        {
          "id_element_list": [],
          "displayed": true,
          "request_locale": false,
          "__module__": "fase.fase",
          "__class__": "Button",
          "text": "Reset",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "locale": null
        }
      ]
    ],
    "displayed": true,
    "request_locale": false,
    "title": null,
    "__class__": "Screen",
    "_screen_id": "f2997e705fd53a8ac139f88bb537144c",
    "__module__": "fase.fase",
    "scrollable": null,
    "on_more": null,
    "locale": null
  },
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "f2997e705fd53a8ac139f88bb537144c"
  }
}

```

### Hello Screen
Client keeps sending `/screenupdate` with *ScreenUpdate*, but they're empty since no text fields are present:
```
method: post
request: /screenupdate
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': 'f2997e705fd53a8ac139f88bb537144c'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "elements_update": null
}

```
Server sends *Response*:
```
{
  "screen": null,
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "f2997e705fd53a8ac139f88bb537144c"
  }
}
```

### User Clicks Reset
User clicks on 'Reset' button, client sends `/elementcallback` with *ElementCallback*:
```
method: post
request: /elementcallback
headers: {'session-id': 'b3885022345831153df4da87b30899d4', 'screen-id': 'f2997e705fd53a8ac139f88bb537144c'}
```
```
{
  "device": {
    "device_token": "dfbcb888-9882-4f88-8000-d5e605aa4990",
    "device_type": "Python"
  },
  "method": "on_click",
  "elements_update": null,
  "id_list": [
    "reset_button_id"
  ],
  "locale": null
}
```
Server sends *Response* with Initial *Screen*:
```
{
  "screen": {
    "on_refresh": null,
    "id_element_list": [
      [
        "text_name_id",
        {
          "id_element_list": [],
          "displayed": true,
          "request_locale": false,
          "__module__": "fase.fase",
          "__class__": "Text",
          "type": null,
          "text": null,
          "multiline": null,
          "locale": null,
          "size": null,
          "hint": "Enter Name"
        }
      ],
      [
        "next_button_id",
        {
          "id_element_list": [],
          "displayed": true,
          "request_locale": false,
          "__module__": "fase.fase",
          "__class__": "Button",
          "text": "Next",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "locale": null
        }
      ]
    ],
    "displayed": true,
    "request_locale": false,
    "title": null,
    "__class__": "Screen",
    "_screen_id": "467c323f6b645bfe9ef714395e118233",
    "__module__": "fase.fase",
    "scrollable": null,
    "on_more": null,
    "locale": null
  },
  "resources": null,
  "elements_update": null,
  "session_info": {
    "session_id": "b3885022345831153df4da87b30899d4"
  },
  "screen_info": {
    "screen_id": "467c323f6b645bfe9ef714395e118233"
  }
}
```

## Hello World Application. Element Callback Examples

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
method: post
request: /getservice
```
```
{
  "device_type": "Python",
  "device_token": "d3f99e4f-9b4a-43d8-8655-d1133893106c"
}
```
Server sends *Response* with Initial *Screen*:
```
{
  "elements_update": null,
  "resources": null,
  "screen": {
    "_screen_id": "2e75f528e4bc98ea4a4084e4e5f33f94",
    "title": null,
    "on_refresh": null,
    "on_more": null,
    "locale": null,
    "request_locale": false,
    "__class__": "Screen",
    "displayed": true,
    "__module__": "fase.fase",
    "scrollable": null,
    "id_element_list": [
      [
        "text_name_id",
        {
          "multiline": null,
          "id_element_list": [],
          "locale": null,
          "request_locale": false,
          "__class__": "Text",
          "displayed": true,
          "__module__": "fase.fase",
          "size": null,
          "type": null,
          "text": null,
          "hint": "Enter Name"
        }
      ],
      [
        "next_button_id",
        {
          "id_element_list": [],
          "locale": null,
          "request_locale": false,
          "__module__": "fase.fase",
          "displayed": true,
          "on_click": {
            "__func__": "FunctionPlaceholder",
            "__module__": "fase.fase"
          },
          "__class__": "Button",
          "text": "Next"
        }
      ]
    ]
  },
  "session_info": {
    "session_id": "91ea4e179ad1e89d2a9c997c92ffaa70"
  },
  "screen_info": {
    "screen_id": "2e75f528e4bc98ea4a4084e4e5f33f94"
  }
}
```

### User Types Name and Clicks Next
User is very quick, types the name and clicks Next. Client sends `/elementcallback` with *ElementCallback* with
*elements_update* field with just entered information:
```
method: post
request: /elementcallback
headers: {'session-id': '91ea4e179ad1e89d2a9c997c92ffaa70', 'screen-id': '2e75f528e4bc98ea4a4084e4e5f33f94'}
```
```
{
  "id_list": [
    "next_button_id"
  ],
  "elements_update": {
    "value_list": [
      "Edward"
    ],
    "id_list_list": [
      [
        "text_name_id"
      ]
    ]
  },
  "method": "on_click",
  "locale": null,
  "device": {
    "device_type": "Python",
    "device_token": "d3f99e4f-9b4a-43d8-8655-d1133893106c"
  }
}
```
Server sends *Response* with Greeting *Screen*:
```
{
  "elements_update": null,
  "resources": null,
  "screen": {
    "_screen_id": "262dc85332834eec76fcfe421c959b1d",
    "title": null,
    "on_refresh": null,
    "on_more": null,
    "locale": null,
    "request_locale": false,
    "__class__": "Screen",
    "displayed": true,
    "__module__": "fase.fase",
    "scrollable": null,
    "id_element_list": [
      [
        "hello_label_id",
        {
          "request_locale": false,
          "__class__": "Label",
          "locale": null,
          "alight": null,
          "__module__": "fase.fase",
          "displayed": true,
          "on_click": null,
          "size": null,
          "id_element_list": [],
          "text": "Hello, Edward!",
          "font": null
        }
      ],
      [
        "reset_button_id",
        {
          "id_element_list": [],
          "locale": null,
          "request_locale": false,
          "__module__": "fase.fase",
          "displayed": true,
          "on_click": {
            "__func__": "FunctionPlaceholder",
            "__module__": "fase.fase"
          },
          "__class__": "Button",
          "text": "Reset"
        }
      ]
    ]
  },
  "session_info": {
    "session_id": "91ea4e179ad1e89d2a9c997c92ffaa70"
  },
  "screen_info": {
    "screen_id": "262dc85332834eec76fcfe421c959b1d"
  }
}
```

## Hello World Application. External Data Examples

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
method: post
request: /getservice
```
```
{
  "device_type": "Python",
  "device_token": "49d77225-fb31-40b5-b5ba-214927b1b782"
}
```
Server sends *Response* with Initial *Screen*:
```
{
  "screen_info": {
    "screen_id": "40da894a663fb2656d95f77965dab93b"
  },
  "screen": {
    "on_more": null,
    "_screen_id": "40da894a663fb2656d95f77965dab93b",
    "on_refresh": null,
    "locale": null,
    "__module__": "fase.fase",
    "id_element_list": [
      [
        "text_name_id",
        {
          "hint": "Enter Name",
          "type": null,
          "displayed": true,
          "text": null,
          "locale": null,
          "__module__": "fase.fase",
          "id_element_list": [],
          "request_locale": false,
          "__class__": "Text",
          "size": null,
          "multiline": null
        }
      ],
      [
        "next_button_id",
        {
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "text": "Next",
          "id_element_list": [],
          "__module__": "fase.fase",
          "locale": null,
          "request_locale": false,
          "__class__": "Button",
          "displayed": true
        }
      ]
    ],
    "request_locale": false,
    "__class__": "Screen",
    "scrollable": null,
    "displayed": true,
    "title": null
  },
  "resources": null,
  "session_info": {
    "session_id": "ec2778ba20558eccf1d1f723a8bdba8f"
  },
  "elements_update": null
}
```

### Name Received
Client keeps sending `/screenupdate` with *ScreenUpdate*

When user hasn't typed anything:
```
method: post
request: /screenupdate
headers: {'screen-id': '40da894a663fb2656d95f77965dab93b', 'session-id': 'ec2778ba20558eccf1d1f723a8bdba8f'}
```
```
{
  "device": {
    "device_type": "Python",
    "device_token": "49d77225-fb31-40b5-b5ba-214927b1b782"
  },
  "elements_update": null
}
```
Server sends *Response* with *elements_update* field 
```
{
  "screen_info": {
    "screen_id": "40da894a663fb2656d95f77965dab93b"
  },
  "screen": null,
  "resources": null,
  "session_info": {
    "session_id": "ec2778ba20558eccf1d1f723a8bdba8f"
  },
  "elements_update": {
    "value_list": [
      "John"
    ],
    "id_list_list": [
      [
        "text_name_id"
      ]
    ]
  },
}

```
**Client fills corresponding text field with 'John'!**

## Notes Application. Resources Management Examples. Signing Up

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
method: post
request: /getservice
```
```
{
  "device_token": "cfc6ba49-3ab3-4fee-a6d1-14cb6f46ab76",
  "device_type": "Python"
}
```
Server sends *Response* with Dashboard *Screen*:
```
{
  "elements_update": null,
  "resources": {
    "resource_list": [
      {
        "filename": "images/notes.png"
      },
      {
        "filename": "images/recent.png"
      },
      {
        "filename": "images/favourite_non.png"
      },
      {
        "filename": "images/sign_in.png"
      },
      {
        "filename": "images/new.png"
      }
    ]
  },
  "screen": {
    "_screen_id": "5ef31afa8844071f41f235b93cc29b93",
    "id_element_list": [
      [
        "main_button",
        {
          "id_element_list": [
            [
              "image",
              {
                "id_element_list": [],
                "filename": "images/new.png",
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "request_locale": false,
                "url": null,
                "__class__": "Image"
              }
            ]
          ],
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "request_locale": false,
          "__class__": "Button",
          "text": "New"
        }
      ],
      [
        "navigation",
        {
          "id_element_list": [
            [
              "notes_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/notes.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Notes"
              }
            ],
            [
              "favourites_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/favourite_non.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Favourites"
              }
            ],
            [
              "recent_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/recent.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Recent"
              }
            ],
            [
              "sign_in_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/sign_in.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Sign In"
              }
            ]
          ],
          "__module__": "fase.fase",
          "__class__": "Navigation"
        }
      ],
      [
        "notes_frame",
        {
          "size": null,
          "border": null,
          "orientation": 1,
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": null,
          "request_locale": false,
          "id_element_list": [],
          "__class__": "Frame"
        }
      ]
    ],
    "__class__": "Screen",
    "scrollable": true,
    "displayed": true,
    "locale": null,
    "__module__": "fase.fase",
    "title": "Notes",
    "request_locale": false,
    "on_refresh": null,
    "on_more": null
  },
  "session_info": {
    "session_id": "7967bc8fbacc9fe514d7690cc7b0efe5"
  },
  "screen_info": {
    "screen_id": "5ef31afa8844071f41f235b93cc29b93"
  }
}
```
Client requests resources from server in parallel:
```
method: get
request: /getresource/filename/images/notes.png
```
```
method: get
request: /getresource/filename/images/recent.png
```
```
method: get
request: /getresource/filename/images/favourite_non.png
```
```
method: get
request: /getresource/filename/images/sign_in.png
```
```
method: get
request: /getresource/filename/images/new.png
```

### User Click Sign In on Dashboard Screen

User clicks "Sign In" on Dashboard Screen. Client sends `/elementcallback` with *ElementCallback*:
```
method: post
request: /elementcallback
headers: {'screen-id': '5ef31afa8844071f41f235b93cc29b93', 'session-id': '7967bc8fbacc9fe514d7690cc7b0efe5'}
```
```
{
  "method": "on_click",
  "elements_update": null,
  "id_list": [
    "navigation",
    "sign_in_button"
  ],
  "device": {
    "device_token": "cfc6ba49-3ab3-4fee-a6d1-14cb6f46ab76",
    "device_type": "Python"
  },
  "locale": null
}
```
Server sends *Response* with Sign In/Sign Up *Screen*:
```
{
  "elements_update": null,
  "resources": null,
  "screen": {
    "_screen_id": "41dfff70d023a8058f42b2a651f8d447",
    "id_element_list": [
      [
        "sign_in_frame_id",
        {
          "size": null,
          "border": null,
          "orientation": 1,
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": null,
          "request_locale": false,
          "id_element_list": [
            [
              "sign_in_button_id",
              {
                "id_element_list": [],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Sign In"
              }
            ],
            [
              "sign_up_button_id",
              {
                "id_element_list": [],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Sign Up"
              }
            ]
          ],
          "__class__": "Frame"
        }
      ],
      [
        "prev_step_button",
        {
          "id_element_list": [],
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "request_locale": false,
          "__class__": "Button",
          "text": "Cancel"
        }
      ]
    ],
    "__class__": "Screen",
    "scrollable": null,
    "displayed": true,
    "locale": null,
    "__module__": "fase.fase",
    "title": null,
    "request_locale": false,
    "on_refresh": null,
    "on_more": null
  },
  "session_info": {
    "session_id": "7967bc8fbacc9fe514d7690cc7b0efe5"
  },
  "screen_info": {
    "screen_id": "41dfff70d023a8058f42b2a651f8d447"
  }
}
```

### User Clicks Sign Up on Sign In/Sign Up Screen
User clicks "Sign Un" on Sign In/Sign Up Screen. Client sends `/elementcallback` with *ElementCallback*:
```
method: post
request: /elementcallback
headers: {'screen-id': '41dfff70d023a8058f42b2a651f8d447', 'session-id': '7967bc8fbacc9fe514d7690cc7b0efe5'}
```
```
{
  "method": "on_click",
  "elements_update": null,
  "id_list": [
    "sign_in_frame_id",
    "sign_up_button_id"
  ],
  "device": {
    "device_token": "cfc6ba49-3ab3-4fee-a6d1-14cb6f46ab76",
    "device_type": "Python"
  },
  "locale": null
}
```
Server sends *Response* with Sign Up form *Screen*:
```
{
  "elements_update": null,
  "resources": null,
  "screen": {
    "_screen_id": "953cd6eaa9fd33aec7bab20f652347e2",
    "id_element_list": [
      [
        "sign_up_frame_id",
        {
          "size": null,
          "border": null,
          "orientation": 1,
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": null,
          "request_locale": false,
          "id_element_list": [
            [
              "phone_number_text_id",
              {
                "multiline": null,
                "size": null,
                "displayed": true,
                "hint": "Phone Number",
                "type": null,
                "__module__": "fase.fase",
                "locale": null,
                "request_locale": false,
                "id_element_list": [],
                "__class__": "Text",
                "text": null
              }
            ],
            [
              "first_name_text_id",
              {
                "multiline": null,
                "size": null,
                "displayed": true,
                "hint": "First Name",
                "type": null,
                "__module__": "fase.fase",
                "locale": null,
                "request_locale": false,
                "id_element_list": [],
                "__class__": "Text",
                "text": null
              }
            ],
            [
              "last_name_text_id",
              {
                "multiline": null,
                "size": null,
                "displayed": true,
                "hint": "Last Name",
                "type": null,
                "__module__": "fase.fase",
                "locale": null,
                "request_locale": false,
                "id_element_list": [],
                "__class__": "Text",
                "text": null
              }
            ],
            [
              "sign_up_button_id",
              {
                "id_element_list": [],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": true,
                "__class__": "Button",
                "text": "Sign Up"
              }
            ]
          ],
          "__class__": "Frame"
        }
      ],
      [
        "prev_step_button",
        {
          "id_element_list": [],
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "request_locale": false,
          "__class__": "Button",
          "text": "Back"
        }
      ]
    ],
    "__class__": "Screen",
    "scrollable": null,
    "displayed": true,
    "locale": null,
    "__module__": "fase.fase",
    "title": null,
    "request_locale": false,
    "on_refresh": null,
    "on_more": null
  },
  "session_info": {
    "session_id": "7967bc8fbacc9fe514d7690cc7b0efe5"
  },
  "screen_info": {
    "screen_id": "953cd6eaa9fd33aec7bab20f652347e2"
  }
}
```

### User Enters Information and Clicks Sign Up
User enters all information and clicks Sign Up. Client sends `/elementcallback` with *ElementCallback* with
*elements_update* field with just entered information:
```
method: post
request: /elementcallback
headers: {'screen-id': '953cd6eaa9fd33aec7bab20f652347e2', 'session-id': '7967bc8fbacc9fe514d7690cc7b0efe5'}
```
```
{
  "method": "on_click",
  "elements_update": {
    "value_list": [
      "4086806761",
      "Igushev",
      "Edward"
    ],
    "id_list_list": [
      [
        "sign_up_frame_id",
        "phone_number_text_id"
      ],
      [
        "sign_up_frame_id",
        "last_name_text_id"
      ],
      [
        "sign_up_frame_id",
        "first_name_text_id"
      ]
    ]
  },
  "id_list": [
    "sign_up_frame_id",
    "sign_up_button_id"
  ],
  "device": {
    "device_token": "cfc6ba49-3ab3-4fee-a6d1-14cb6f46ab76",
    "device_type": "Python"
  },
  "locale": {
    "country_code": "US"
  }
}
```
Server sends *Response* with Activation Code *Screen*:
```
{
  "elements_update": null,
  "resources": null,
  "screen": {
    "_screen_id": "7cde2466ed78b36c3320ff86bac3b6ed",
    "id_element_list": [
      [
        "enter_activation_frame_id",
        {
          "size": null,
          "border": null,
          "orientation": 1,
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": null,
          "request_locale": false,
          "id_element_list": [
            [
              "activation_code_text_id",
              {
                "multiline": null,
                "size": null,
                "displayed": true,
                "hint": "Activation Code",
                "type": null,
                "__module__": "fase.fase",
                "locale": null,
                "request_locale": false,
                "id_element_list": [],
                "__class__": "Text",
                "text": null
              }
            ],
            [
              "send_button_id",
              {
                "id_element_list": [],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Send"
              }
            ]
          ],
          "__class__": "Frame"
        }
      ],
      [
        "prev_step_button",
        {
          "id_element_list": [],
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "request_locale": false,
          "__class__": "Button",
          "text": "Back"
        }
      ]
    ],
    "__class__": "Screen",
    "scrollable": null,
    "displayed": true,
    "locale": null,
    "__module__": "fase.fase",
    "title": null,
    "request_locale": false,
    "on_refresh": null,
    "on_more": null
  },
  "session_info": {
    "session_id": "7967bc8fbacc9fe514d7690cc7b0efe5"
  },
  "screen_info": {
    "screen_id": "7cde2466ed78b36c3320ff86bac3b6ed"
  }
}
```

### User Enters Activation Code and Clicks Send
User enters activation code and clicks Send. Client sends `/elementcallback` with *ElementCallback* with
*elements_update* field with just entered information:
```
method: post
request: /elementcallback
headers: {'screen-id': '7cde2466ed78b36c3320ff86bac3b6ed', 'session-id': '7967bc8fbacc9fe514d7690cc7b0efe5'}
```
```
{
  "method": "on_click",
  "elements_update": {
    "value_list": [
      "237418"
    ],
    "id_list_list": [
      [
        "enter_activation_frame_id",
        "activation_code_text_id"
      ]
    ]
  },
  "id_list": [
    "enter_activation_frame_id",
    "send_button_id"
  ],
  "device": {
    "device_token": "cfc6ba49-3ab3-4fee-a6d1-14cb6f46ab76",
    "device_type": "Python"
  },
  "locale": null
}
```
Server sends *Response* with Dashboard *Screen*:
```
{
  "elements_update": null,
  "resources": {
    "resource_list": [
      {
        "filename": "images/notes.png"
      },
      {
        "filename": "images/recent.png"
      },
      {
        "filename": "images/sign_out.png"
      },
      {
        "filename": "images/favourite_non.png"
      },
      {
        "filename": "images/new.png"
      }
    ]
  },
  "screen": {
    "_screen_id": "3c595140a8eaea06b96af688222ef04d",
    "id_element_list": [
      [
        "main_button",
        {
          "id_element_list": [
            [
              "image",
              {
                "id_element_list": [],
                "filename": "images/new.png",
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "request_locale": false,
                "url": null,
                "__class__": "Image"
              }
            ]
          ],
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "request_locale": false,
          "__class__": "Button",
          "text": "New"
        }
      ],
      [
        "navigation",
        {
          "id_element_list": [
            [
              "notes_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/notes.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Notes"
              }
            ],
            [
              "favourites_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/favourite_non.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Favourites"
              }
            ],
            [
              "recent_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/recent.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Recent"
              }
            ],
            [
              "sign_out_button",
              {
                "id_element_list": [
                  [
                    "image",
                    {
                      "id_element_list": [],
                      "filename": "images/sign_out.png",
                      "displayed": true,
                      "locale": null,
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "url": null,
                      "__class__": "Image"
                    }
                  ]
                ],
                "displayed": true,
                "locale": null,
                "__module__": "fase.fase",
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "request_locale": false,
                "__class__": "Button",
                "text": "Sign Out"
              }
            ]
          ],
          "__module__": "fase.fase",
          "__class__": "Navigation"
        }
      ],
      [
        "notes_frame",
        {
          "size": null,
          "border": null,
          "orientation": 1,
          "displayed": true,
          "locale": null,
          "__module__": "fase.fase",
          "on_click": null,
          "request_locale": false,
          "id_element_list": [],
          "__class__": "Frame"
        }
      ]
    ],
    "__class__": "Screen",
    "scrollable": true,
    "displayed": true,
    "locale": null,
    "__module__": "fase.fase",
    "title": "Notes",
    "request_locale": false,
    "on_refresh": null,
    "on_more": null
  },
  "session_info": {
    "session_id": "35335c2b1c30888950754fbefe51427d"
  },
  "screen_info": {
    "screen_id": "3c595140a8eaea06b96af688222ef04d"
  }
}
```
**Client does NOT request resources since they have been cached!**

## Notes Application. Resources Management Examples. Adding New Note

### Client Starts
Client starts and sends `/getservice` with *Device*:
```
method: post
request: /getservice
```
```
{
  "device_type": "Python",
  "device_token": "e47e16a0-0e85-4014-8a14-06289f76c41a"
}
```
Server sends *Response* with Dashboard *Screen*:
```
{
  "elements_update": null,
  "resources": {
    "resource_list": [
      {
        "filename": "images/notes.png"
      },
      {
        "filename": "images/recent.png"
      },
      {
        "filename": "images/favourite_non.png"
      },
      {
        "filename": "images/sign_in.png"
      },
      {
        "filename": "images/new.png"
      }
    ]
  },
  "screen_info": {
    "screen_id": "ea70243fb03aa62c00d732cd0adf6acc"
  },
  "session_info": {
    "session_id": "2e91841ec279faf08412e0bdda8dc556"
  },
  "screen": {
    "on_refresh": null,
    "_screen_id": "ea70243fb03aa62c00d732cd0adf6acc",
    "__class__": "Screen",
    "locale": null,
    "id_element_list": [
      [
        "main_button",
        {
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "text": "New",
          "__class__": "Button",
          "locale": null,
          "id_element_list": [
            [
              "image",
              {
                "url": null,
                "__class__": "Image",
                "locale": null,
                "id_element_list": [],
                "__module__": "fase.fase",
                "filename": "images/new.png",
                "request_locale": false,
                "displayed": true
              }
            ]
          ],
          "__module__": "fase.fase",
          "request_locale": false,
          "displayed": true
        }
      ],
      [
        "navigation",
        {
          "__module__": "fase.fase",
          "__class__": "Navigation",
          "id_element_list": [
            [
              "notes_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Notes",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/notes.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ],
            [
              "favourites_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Favourites",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/favourite_non.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ],
            [
              "recent_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Recent",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/recent.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ],
            [
              "sign_in_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Sign In",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/sign_in.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ]
          ]
        }
      ],
      [
        "notes_frame",
        {
          "on_click": null,
          "size": null,
          "__class__": "Frame",
          "locale": null,
          "id_element_list": [],
          "__module__": "fase.fase",
          "orientation": 1,
          "border": null,
          "request_locale": false,
          "displayed": true
        }
      ]
    ],
    "__module__": "fase.fase",
    "on_more": null,
    "title": "Notes",
    "request_locale": false,
    "displayed": true,
    "scrollable": true
  }
}
```
Client requests resources from server in parallel:
```
method: get
request: /getresource/filename/images/notes.png
```
```
method: get
request: /getresource/filename/images/recent.png
```
```
method: get
request: /getresource/filename/images/favourite_non.png
```
```
method: get
request: /getresource/filename/images/sign_in.png
```
```
method: get
request: /getresource/filename/images/new.png
```

### User Click Main Button

User Click Main Button to add a new note on Dashboard Screen. Client sends `/elementcallback` with *ElementCallback*:
```
method: post
request: /elementcallback
headers: {'screen-id': 'ea70243fb03aa62c00d732cd0adf6acc', 'session-id': '2e91841ec279faf08412e0bdda8dc556'}
```
```
{
  "elements_update": null,
  "device": {
    "device_type": "Python",
    "device_token": "e47e16a0-0e85-4014-8a14-06289f76c41a"
  },
  "id_list": [
    "main_button"
  ],
  "method": "on_click",
  "locale": null
}
```
Server sends *Response* with New Note *Screen*:
```
{
  "elements_update": null,
  "resources": {
    "resource_list": [
      {
        "filename": "images/favourite_non.png"
      }
    ]
  },
  "screen_info": {
    "screen_id": "4191c70ab0ef988acd80d3b7f01119a5"
  },
  "session_info": {
    "session_id": "2e91841ec279faf08412e0bdda8dc556"
  },
  "screen": {
    "on_refresh": null,
    "_screen_id": "4191c70ab0ef988acd80d3b7f01119a5",
    "__class__": "Screen",
    "locale": null,
    "id_element_list": [
      [
        "note_frame",
        {
          "on_click": null,
          "size": null,
          "__class__": "Frame",
          "locale": null,
          "id_element_list": [
            [
              "header_text",
              {
                "size": null,
                "multiline": null,
                "displayed": true,
                "__class__": "Text",
                "locale": null,
                "id_element_list": [],
                "text": null,
                "request_locale": false,
                "type": null,
                "__module__": "fase.fase",
                "hint": "Header"
              }
            ],
            [
              "text_text",
              {
                "size": 2,
                "multiline": true,
                "displayed": true,
                "__class__": "Text",
                "locale": null,
                "id_element_list": [],
                "text": null,
                "request_locale": false,
                "type": null,
                "__module__": "fase.fase",
                "hint": "Text"
              }
            ]
          ],
          "__module__": "fase.fase",
          "orientation": 1,
          "border": null,
          "request_locale": false,
          "displayed": true
        }
      ],
      [
        "next_step_button",
        {
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "text": "Save",
          "__class__": "Button",
          "locale": null,
          "id_element_list": [],
          "__module__": "fase.fase",
          "request_locale": false,
          "displayed": true
        }
      ],
      [
        "prev_step_button",
        {
          "on_click": null,
          "text": null,
          "__class__": "Button",
          "locale": null,
          "id_element_list": [
            [
              "context_menu",
              {
                "text": null,
                "__class__": "Menu",
                "id_element_list": [
                  [
                    "favourite_menu_item",
                    {
                      "on_click": {
                        "__module__": "fase.fase",
                        "__func__": "FunctionPlaceholder"
                      },
                      "text": "Add to Favourites",
                      "__class__": "MenuItem",
                      "locale": null,
                      "id_element_list": [
                        [
                          "image",
                          {
                            "url": null,
                            "__class__": "Image",
                            "locale": null,
                            "id_element_list": [],
                            "__module__": "fase.fase",
                            "filename": "images/favourite_non.png",
                            "request_locale": false,
                            "displayed": true
                          }
                        ]
                      ],
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "displayed": true
                    }
                  ],
                  [
                    "cancel_menu_item",
                    {
                      "on_click": {
                        "__module__": "fase.fase",
                        "__func__": "FunctionPlaceholder"
                      },
                      "text": "Cancel",
                      "__class__": "MenuItem",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase"
              }
            ]
          ],
          "__module__": "fase.fase",
          "request_locale": false,
          "displayed": true
        }
      ]
    ],
    "__module__": "fase.fase",
    "on_more": null,
    "title": null,
    "request_locale": false,
    "displayed": true,
    "scrollable": null
  }
}
```

### User Enters Data and Clicks Next Button
User enters data and clicks next button with text "Save". Client sends `/elementcallback` with *ElementCallback* with
*elements_update* field with just entered information:
```
method: post
request: /elementcallback
headers: {'screen-id': '4191c70ab0ef988acd80d3b7f01119a5', 'session-id': '2e91841ec279faf08412e0bdda8dc556'}
```
```
{
  "elements_update": {
    "value_list": [
      "Header 1",
      "Text 1"
    ],
    "id_list_list": [
      [
        "note_frame",
        "header_text"
      ],
      [
        "note_frame",
        "text_text"
      ]
    ]
  },
  "device": {
    "device_type": "Python",
    "device_token": "e47e16a0-0e85-4014-8a14-06289f76c41a"
  },
  "id_list": [
    "next_step_button"
  ],
  "method": "on_click",
  "locale": null
}
```
Server sends *Response* with Dashboard *Screen* which has one just added note:
```
{
  "elements_update": null,
  "resources": {
    "resource_list": [
      {
        "filename": "images/notes.png"
      },
      {
        "filename": "images/recent.png"
      },
      {
        "filename": "images/favourite_non.png"
      },
      {
        "filename": "images/sign_in.png"
      },
      {
        "filename": "images/new.png"
      }
    ]
  },
  "screen_info": {
    "screen_id": "eaf6548e8712458c5a439bbe43336d70"
  },
  "session_info": {
    "session_id": "2e91841ec279faf08412e0bdda8dc556"
  },
  "screen": {
    "on_refresh": null,
    "_screen_id": "eaf6548e8712458c5a439bbe43336d70",
    "__class__": "Screen",
    "locale": null,
    "id_element_list": [
      [
        "main_button",
        {
          "on_click": {
            "__module__": "fase.fase",
            "__func__": "FunctionPlaceholder"
          },
          "text": "New",
          "__class__": "Button",
          "locale": null,
          "id_element_list": [
            [
              "image",
              {
                "url": null,
                "__class__": "Image",
                "locale": null,
                "id_element_list": [],
                "__module__": "fase.fase",
                "filename": "images/new.png",
                "request_locale": false,
                "displayed": true
              }
            ]
          ],
          "__module__": "fase.fase",
          "request_locale": false,
          "displayed": true
        }
      ],
      [
        "navigation",
        {
          "__module__": "fase.fase",
          "__class__": "Navigation",
          "id_element_list": [
            [
              "notes_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Notes",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/notes.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ],
            [
              "favourites_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Favourites",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/favourite_non.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ],
            [
              "recent_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Recent",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/recent.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ],
            [
              "sign_in_button",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "text": "Sign In",
                "__class__": "Button",
                "locale": null,
                "id_element_list": [
                  [
                    "image",
                    {
                      "url": null,
                      "__class__": "Image",
                      "locale": null,
                      "id_element_list": [],
                      "__module__": "fase.fase",
                      "filename": "images/sign_in.png",
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "request_locale": false,
                "displayed": true
              }
            ]
          ]
        }
      ],
      [
        "notes_frame",
        {
          "on_click": null,
          "size": null,
          "__class__": "Frame",
          "locale": null,
          "id_element_list": [
            [
              "note_frame_5e825ad6c8941c378ba7c43e4de77ae5",
              {
                "on_click": {
                  "__module__": "fase.fase",
                  "__func__": "FunctionPlaceholder"
                },
                "size": null,
                "__class__": "Frame",
                "locale": null,
                "id_element_list": [
                  [
                    "note_header_frame",
                    {
                      "on_click": null,
                      "size": 2,
                      "__class__": "Frame",
                      "locale": null,
                      "id_element_list": [
                        [
                          "note_header_label",
                          {
                            "on_click": null,
                            "text": "Header 1",
                            "font": 1.5,
                            "locale": null,
                            "id_element_list": [],
                            "alight": 1,
                            "__class__": "Label",
                            "size": 2,
                            "request_locale": false,
                            "displayed": true,
                            "__module__": "fase.fase"
                          }
                        ],
                        [
                          "note_header_image",
                          {
                            "url": null,
                            "__class__": "Image",
                            "locale": null,
                            "id_element_list": [],
                            "__module__": "fase.fase",
                            "filename": "images/favourite_non.png",
                            "request_locale": false,
                            "displayed": true
                          }
                        ]
                      ],
                      "__module__": "fase.fase",
                      "orientation": 2,
                      "border": null,
                      "request_locale": false,
                      "displayed": true
                    }
                  ],
                  [
                    "note_frame_label",
                    {
                      "on_click": null,
                      "text": "Text 1",
                      "font": null,
                      "locale": null,
                      "id_element_list": [],
                      "alight": 1,
                      "__class__": "Label",
                      "size": null,
                      "request_locale": false,
                      "displayed": true,
                      "__module__": "fase.fase"
                    }
                  ],
                  [
                    "note_deails_frame",
                    {
                      "on_click": null,
                      "size": null,
                      "__class__": "Frame",
                      "locale": null,
                      "id_element_list": [
                        [
                          "note_deails_frame_datetime_text",
                          {
                            "on_click": null,
                            "text": "Just now",
                            "font": 0.7,
                            "locale": null,
                            "id_element_list": [],
                            "alight": 2,
                            "__class__": "Label",
                            "size": 2,
                            "request_locale": false,
                            "displayed": true,
                            "__module__": "fase.fase"
                          }
                        ]
                      ],
                      "__module__": "fase.fase",
                      "orientation": 2,
                      "border": null,
                      "request_locale": false,
                      "displayed": true
                    }
                  ]
                ],
                "__module__": "fase.fase",
                "orientation": 1,
                "border": true,
                "request_locale": false,
                "displayed": true
              }
            ]
          ],
          "__module__": "fase.fase",
          "orientation": 1,
          "border": null,
          "request_locale": false,
          "displayed": true
        }
      ]
    ],
    "__module__": "fase.fase",
    "on_more": null,
    "title": "Notes",
    "request_locale": false,
    "displayed": true,
    "scrollable": true
  }
}
```
**Client does NOT request resources since they have been cached!**
