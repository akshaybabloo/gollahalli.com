---
title: "Unreal Engine 4 and Samsung Gear VR"
date: 2016-09-05T11:20:47+12:00
draft: false
categories: ["Tutorial"]
tags: ["UnrealEngine4", "VR", "Android"]
description: "Deploying games from Unreal Engine 4 to Samsung Gear VR."
images: ["/img/blog/UnrealEngine4.gif", "/img/blog/DevOpti.png", "/img/blog/USBDebug.png", "/img/blog/Plugins.png", "/img/blog/Plugins1.png", "/img/blog/TargetHardware.png", "/img/blog/ProjectSettingsMenu.png", "/img/blog/AndroidPlatform.png", "/img/blog/AndroidPlatform1.png", "/img/blog/AndroidPlatformSDK.png", "/img/blog/Packing.png"]
ads: true
author:
  prefix: "Mr."
  firstName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Software Engineer"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
siteMapImages:
  - imageLoc: "/img/blog/UnrealEngine4.gif"
    imageCaption: "UnrealEngine 4 and Samsung GearVR"
  - imageLoc: "/img/blog/DevOpti.png"
    imageCaption: "Settings menu"
  - imageLoc: "/img/blog/USBDebug.png"
    imageCaption: "Debug enable"
  - imageLoc: "/img/blog/Plugins.png"
    imageCaption: "Package configuration"
  - imageLoc: "/img/blog/Plugins1.png"
    imageCaption: "Package configuration"
  - imageLoc: "/img/blog/TargetHardware.png"
    imageCaption: "Target hardware"
  - imageLoc: "/img/blog/ProjectSettingsMenu.png"
    imageCaption: "Project Settings Menu"
  - imageLoc: "/img/blog/AndroidPlatform.png"
    imageCaption: "Android Platform"
  - imageLoc: "/img/blog/AndroidPlatform1.png"
    imageCaption: "Android Platform"
  - imageLoc: "/img/blog/AndroidPlatformSDK.png"
    imageCaption: "Android Platform SDK"
  - imageLoc: "/img/blog/Packing.png"
    imageCaption: "Packing"
sitemap:
  priority: 0.8
  changeFreq: monthly
---

A simple game using Unreal Engine 4.10.\* and 4.11.2 for GearVR

**The code can be found at - [https://github.com/akshaybabloo/GearVR-UnrealEngine4](https://github.com/akshaybabloo/GearVR-UnrealEngine4)**

> Note 1: For Mac users make sure you download Java 6 -> [https://support.apple.com/kb/dl1572](https://support.apple.com/kb/dl1572) and Java 7. The setup is the same for UnrealEngine 4.11.

**Table of content**

- [1 Introduction](#1-introduction)
- [2 Requirements](#2-requirements)
  - [2.1 General](#21-general)
  - [2.2 Mac](#22-mac)
  - [2.3 Windows](#23-windows)
- [3 Instillation](#3-instillation)
  - [3.1 Mac](#31-mac)
    - [3.1.1 Android Studio](#311-android-studio)
  - [3.2 Enabling Android Developer Options](#32-enabling-android-developer-options)
  - [3.3 Getting device ID](#33-getting-device-id)
  - [3.4 Downloading `Oculus Signature File (osig)` and placing it in UE](#34-downloading-oculus-signature-file-osig-and-placing-it-in-ue)
  - [3.4 Installing `CodeWorks for Android`](#34-installing-codeworks-for-android)
- [4 Developing a game](#4-developing-a-game)
- [5 Packing it up for Android](#5-packing-it-up-for-android)
  - [5.1 Package Configuration](#51-package-configuration)
  - [5.2 Packing](#52-packing)
- [6 Installing it on Android](#6-installing-it-on-android)

**License**

The code is provided under [MIT License](https://github.com/akshaybabloo/JavaScript-Tutorial/blob/master/LICENSE), and the tutorial is provided under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)

<!--adsense-->

## 1 Introduction

In this tutorial, I will be going to develop a simple environment where the first person player can walk around. This game was developed on Mac and should be similar to windows. Please see "Note" where I would be including some important points about the structure and running of the game.

## 2 Requirements

### 2.1 General

1. A 2015 Samsung Galaxy phone i.e. S6, S6 edge, S6 edge+ or Note 5.
2. Samsung Gear VR.
3. Experience with Unreal Engine 4. If you don't have any previous experience, you can go through my tutorial on Unreal Engine 4 [here](https://github.com/akshaybabloo/UnrealEngine_4_Notes)

### 2.2 Mac

**Software**

1. [Unreal Engine 4](https://www.unrealengine.com/dashboard)
2. [Android Studio](http://developer.android.com/sdk/index.html)
3. AndroidWorks

**Hardware**

1. A 2015 Samsung Galaxy phone i.e. S6, S6 edge, S6 edge+ or Note 5.
2. Samsung Gear VR.

<!--adsense-->

### 2.3 Windows

**Software**

1. [Unreal Engine 4](https://www.unrealengine.com/dashboard)
2. [Android Studio](http://developer.android.com/sdk/index.html)
3. AndroidWorks
4. Samsung drivers

**Hardware**

1. A 2015 Samsung Galaxy phone i.e. S6, S6 edge, S6 edge+, S7, S7 edge or Note 5.
2. Samsung Gear VR.

## 3 Instillation

### 3.1 Mac

#### 3.1.1 Android Studio

1. Download [Android Studio](http://developer.android.com/sdk/index.html).
2. Open it and move it to `Application`.
3. Open the application and follow the installation process.
4. Once the installation process is done, open the application and do the follow
5. Click on `Android Studio -> Preference`
6. Click on `Appreance & Behavior -> System Settings -> Android SDK` and tick on `Android 5.0.1` and `Android 5.1.1`.

**Installing command line tools**

1. Open `Terminal`.
2. Type `nano .bash_profile` and type the following in it:

```shell
  # Android
  export PATH="/Users/<user>/Library/Android/sdk/platform-tools:$PATH"
  export PATH="/Users/<user>/Library/Android/sdk/tools:$PATH"
```

> Note 2: `<user>` should be replaced by your username.

4. To save press `Control + x` and then press `y`.
5. Restart `Terminal` and type `android` to see if the tools are working.

### 3.2 Enabling Android Developer Options

1. Go to `Settings -> About -> Software Info` and click on `Build Number` **seven** times.
2. Now go back, You should now see `Developer Options`.

<div align="center">
  {{< figure src="/img/blog/DevOpti.png" title="Settings menu" alt="Settings menu" width="300" >}}
</div>

3. Click on `Developer Options` and enable `USB debugging.'

<div align="center">
  {{< figure src="/img/blog/USBDebug.png" title="Debug enable" alt="Debug enable" width="300" >}}
</div>

4. Once you connect your phone to the system, it will ask you to confirm the connected computers RSA KEY. Click `Ok` to continue.

<!--adsense-->

### 3.3 Getting device ID

Make sure you have your phone connected to the computer, and the `USB debugging` is switched on. Open `Terminal` and type in `adb devices`, this will print an alphanumeric/numeric key something like this.

```md
List of devices attached
1234567891011123    device
```

### 3.4 Downloading `Oculus Signature File (osig)` and placing it in UE

Copy the above number and go to [https://developer.oculus.com/osig/](https://developer.oculus.com/osig/) and paste it in the text field then click on `Download File`. `oculussig_1234567891011123` file will be downloaded.

Move this file to `/Users/Shared/UnrealEngine/4.10/Engine/Build/Android/Java/assets/`

> Note for UnrealEngine 4.11: If you can find `assets` folder, create one and move the file to it.

### 3.4 Installing `CodeWorks for Android`

Goto `/Users/Shared/UnrealEngine/4.10/Engine/Extras/AndroidWorks/Mac/`. Open `AndroidWorks-1R1-osx.dmg` and follow the instillation steps.

This is what I have installed:

```md
The following components are installed:
Android SDK
    +Android SDK Base 24.2.0
    +Android Platform Tools 22.0.0
    +Android Build Tools 22.0.1
    +Android 4.4.2(API 19) 4.4.2
    +Android 5.0 (API 21) 5.0.1
    +Android SDK Support Library 22.2.0
    +Android SDK Support Repository Library 15
Android Toolchain
    +Android NDK 10e
    +Apache Ant 1.8.2
    +Gradle 2.2.1
```

## 4 Developing a game

Please see my tutorial on [UnrealEngine 4](https://github.com/akshaybabloo/UnrealEngine_4_Notes).

## 5 Packing it up for Android

### 5.1 Package Configuration

Once you have completed designing the game do the following:

Open `Plugins`

<div align="center">
  {{< figure src="/img/blog/Plugins.png" title="Package configuration" alt="Package configuration" >}}
</div>

Then, make sure you have enabled the following:

<div align="center">
  {{< figure src="/img/blog/Plugins1.png" title="Package configuration" alt="Package configuration" >}}
</div>

Next open your `Project Settings...`, Go to `Target Hardware` and do the following:

<div align="center">
  {{< figure src="/img/blog/TargetHardware.png" title="Target hardware" alt="Target hardware" >}}
</div>

Then do this:

<div align="center">
  {{< figure src="/img/blog/ProjectSettingsMenu.png" title="Project Settings Menu" alt="Project Settings Menu" >}}
</div>

Then do the following:

<div align="center">
  {{< figure src="/img/blog/AndroidPlatform.png" title="Android Platform" alt="Android Platform" >}}
</div>

Then do this:

<div align="center">
  {{< figure src="/img/blog/AndroidPlatform1.png" title="Android Platform" alt="Android Platform" >}}
</div>

And then this:

<div align="center">
  {{< figure src="/img/blog/AndroidPlatformSDK.png" title="Android Platform SDK" alt="Android Platform SDK" >}}
</div>

<!--adsense-->

### 5.2 Packing

Do the following:

<div align="center">
  {{< figure src="/img/blog/Packing.png" title="Packing" alt="Packing" >}}
</div>

## 6 Installing it on Android

> Note 3: Make sure you have connected your phone before proceeding.

Open `Android_ETC2` folder and double click on `Install_GearVR-UnrealEngine4_Development-armv7-es2.command`, this will open `Terminal` and install the software for you.
