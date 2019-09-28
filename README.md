# Frontend in the Cloud - Creating Native Mobile Applications on Python - Free and Open Source - 5G Ready

Table of Contents
=================

   * [Introduction](#introduction)
      * [Overview](#overview)
      * [Demo](#demo)
      * [GitHub Client Repositories](#github-client-repositories)
      * [Platforms](#platforms)
      * [Languages](#languages)
   * [Hello World](#hello-world)
   * [Documentatoin](#documentatoin)
   * [Fase Elements](#fase-elements)
      * [Comparing Fase Elements to similar Elements in iOS/Android/Tkinter](#comparing-fase-elements-to-similar-elements-in-iosandroidtkinter)
   * [Drawing Elements](#drawing-elements)
      * [Mobile Device Differences](#mobile-device-differences)
      * [Abstract Elements on iOS](#abstract-elements-on-ios)
      * [Abstract Elements on Android](#abstract-elements-on-android)
   * [Examples](#examples)
      * [Notes Service](#notes-service)
   * [Links](#links)

# Introduction

## Overview

  * Singular frontend which is rendered on _all_ platforms with **native components**;
  * Running frontend in the cloud allows to synchronize not only data, but entire context and provide synchronized and seamless user experience;
  * Advanced app management (instant updates, support of A/B testing);
  * **Free** and **Open Source**;
  * Used by **thousands of Applications**;

## Demo

[![Demo](https://img.youtube.com/vi/hb64nMG7QWY/0.jpg)](https://youtu.be/hb64nMG7QWY)

## GitHub Client Repositories

  * Fase iOS - [https://github.com/igushev/fase_ios](https://github.com/igushev/fase_ios);
  * Fase Android - [https://github.com/igushev/fase_android](https://github.com/igushev/fase_android)

## Platforms

  * **Supported**: iOS, Android;
  * **Coming**: Web Browser, Tizen;

## Languages

  * **Supported**: Python;
  * **Coming**: C++, Java, PHP, Go, JavaScript;

# Hello World

```python
from fase import fase


class HelloWorldService(fase.Service):

  def OnStart(self):
    screen = fase.Screen(self)
    screen.AddText(id_='text_name_id', hint='Enter Name')
    screen.AddButton(id_='next_button_id', text='Next',
                     on_click=HelloWorldService.OnNextButton)
    return screen

  def OnNextButton(self, screen, element):
    name = screen.GetText(id_='text_name_id').GetText()
    screen = fase.Screen(self)
    screen.AddLabel(id_='hello_label_id', text='Hello, %s!' % name)
    screen.AddButton(id_='reset_button_id', text='Reset',
                     on_click=HelloWorldService.OnResetButton)
    return screen
    
  def OnResetButton(self, screen, element):
    # Ignore previous screen and element.
    return self.OnStart()


fase.Service.RegisterService(HelloWorldService)
```

# Documentatoin

API documentation is [here](http://fase.io/documentation/)

How to develop Fase Service read [here](http://fase.io/converter_service/).

How to deploy the server of a Fase Service read [here](http://fase.io/converter_server/).

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


# Drawing Elements

## Mobile Device Differences
|Element|iOS|Android|Windows Phone|
|-------|---|-------|-------------|
|Main button|Button in the right upper corner|Big button in the right bottom corner|Button in the middle of the button bar|
|Navigation|Buttons on bottom bar|Items in main menu from left top button|Buttons on top and bottom bar|
|Next button|Button in the right upper corner|Button in the right upper corner||
|Prev button|Button in the left upper corner|Built in system back button||

## Abstract Elements on iOS
![Abstract Elements on iOS](http://fase.io/images/elements/ios.png "Abstract Elements on iOS")

## Abstract Elements on Android
![Abstract Elements on Android](http://fase.io/images/elements/android.png "Abstract Elements on Android")

# Examples

## Notes Service

  * Fase Source Code - [https://github.com/igushev/notes_fase](https://github.com/igushev/notes_fase)
  * [App Store](https://itunes.apple.com/us/app/notes-service/id1406678770?ls=1&mt=8)
  * [Play Store](https://play.google.com/store/apps/details?id=com.notes_service)

# Links

  * Official website - [http://fase.io](http://fase.io);
  * [Article on Medium about Fase](https://medium.com/@igushev/frontend-in-the-cloud-creating-native-mobile-applications-on-python-free-and-open-source-5g-15b34d956036);


