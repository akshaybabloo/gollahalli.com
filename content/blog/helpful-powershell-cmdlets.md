---
title: "Helpful Powershell Cmdlets"
date: 2023-02-26T12:02:06+13:00
draft: false
categories: ["PowerShell"]
tags: ["PowerShell"]
description: "A list of helpful PowerShell cmdlets that I have found useful."
images: []
ads: true
video: false
# htmlScripts: []
author:
  prefix: "Mr."
  firstName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Research Assistant"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
sitemap:
  priority: 0.8
  changeFreq: monthly
# siteMapImages:
#   - imageLoc: ""
#     imageCaption: ""
---

<!--adsense-->

These are some of the PowerShell cmdlets that I have found useful. I will be adding more as I find them. I usually add them to my PowerShell profile so that I can use them anywhere. To get the path of your PowerShell profile, run the following command:

```
> $profile
C:\Users\<user>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

Don't forget to restart PowerShell after adding the cmdlets to your profile.

**Table of Contents**

- [List all USB devices](#list-all-usb-devices)
- [Get the size of a folder](#get-the-size-of-a-folder)

## List all USB devices

```powershell
function Get-UsbDevices { 
  Get-PnpDevice -InstanceId 'USB*' -Class 'USB' -Status OK 
}
Set-Alias -Name lsusb -Value Get-UsbDevices
```

## Get the size of a folder

This is a recursive function that will get the size of a folder in MB with 2 decimal places.

```powershell
function Get-Size {

  param(
    # The path to the folder
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Path="."
  )

  "{0:N2} mb" -f ((Get-ChildItem -Recurse -Force $path | Measure-Object -Property Length -sum).Sum / 1Mb)
}
```