# Fase Application Examples

## Hello World Application

### Starting Client

Client starts and sends  `/getservice` request with body:
```
{ 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
  'device_type': 'Python'}
```
Server sends response:
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

Client keeps sending `/screenupdate` requests

When user hasn't typed anything:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server response:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User typed 'Ed'
Client:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': {'id_list_list': [['text_name_id']], 'value_list': ['Ed']}}
```
Server:
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
Server:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User added 'ward' adn finished typing 'Edward':
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': { 'id_list_list': [['text_name_id']],
                       'value_list': ['Edward']}}
```
Server:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```
User does not type but text field still has 'Edward'
Client:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '7c2cfa33c307697c560ec0683565f248'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### User Click
Client sends `/elementcallback`:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None,
  'id_list': ['next_button_id'],
  'locale': None,
  'method': 'on_click'}
```
**If User clicks Next before Server sends ScreenUpdate with typed name, elements_update field is not empty!**
Server sends new Screen:
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

All ScreenUpdate are empty since no text fiels are prsent:
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None}
```
Server:
```
{ 'elements_update': None,
  'resources': None,
  'screen': None,
  'screen_info': {'screen_id': '20d0a7775a1ab89639aa2d91e3bbf862'},
  'session_info': {'session_id': '5a87a926282681fe2a6ad94b5a701cf4'}}
```

### User Click
Client sends `/elementcallback`
```
{ 'device': { 'device_token': '42209288-51e7-4573-84b6-3cde39477e1d',
              'device_type': 'Python'},
  'elements_update': None,
  'id_list': ['reset_button_id'],
  'locale': None,
  'method': 'on_click'}
```
Server send Response with initial Screen:
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
