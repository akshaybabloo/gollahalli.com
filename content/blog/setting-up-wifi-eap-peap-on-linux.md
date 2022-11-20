---
title: "Setting up WiFi EAP-PEAP on Linux"
description: "This post is the secret to enabling EAP-PEAP WiFi connection."
date: 2016-06-25T18:29:02+12:00
draft: false
tags: ["Linux"]
categories: ["Tutorial"]
description: "Do you have problem accessing enterprise WiFi on Linux? Then this article is for you."
ads: true
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
---

A few months ago I was trying to setup up WiFi on my Raspberry Pi. That time I didn't know that Pi has problems with Enterprise WiFi and my university did not provide support to Linux distribution. Thanks to Google I fond the answer.

I don't want others to have the same problem. Follow these steps to setup up your office/university WiFi.

<!--adsense-->

## Step 1: Requirements

Make sure you have your username, password, proxy IP and WiFi SSID. For the sake of this tutorial let's consider a username, password, proxy IP and WiFi SSID.

```md
Username: user
Password: 123456
IP: 123.456.789.012:1234
WiFi SSID: CompanyName
```

## Step 2: Getting your companies HTTP/HTTPS proxies

Ask your company for a proxy address (It's usually an IP address). Once you have that do the following:

- Open Terminal, and type sudo nano ~/.bashrc. Go to the end of the nano editor and type the following

```md
export HTTP_PROXY="http://user:123456@123.456.789.012:1234"
export HTTPS_PROXY="http://user:123456@123.456.789.012:1234"
```

- Save it by doing <kbd class="uk-label">ctrl</kbd>+<kbd class="uk-label">X</kbd>, <kbd class="uk-label">return</kbd> and <kbd class="uk-label">return</kbd>.
- Next go to sudo nano /etc/apt/apt.conf.d/10proxy, in that type in the following:

```md
Acquire::http:Proxy "http://user:123456@123.456.789.012:1234"
Acquire::https:Proxy "https://user:123456@123.456.789.012:1234"
```

- Save it by doing <kbd class="uk-label">ctrl</kbd>+<kbd class="uk-label">X</kbd>, <kbd class="uk-label">return</kbd> and <kbd class="uk-label">return</kbd>.

<!--adsense-->

## Step 3: Setting up WPA Supplicant (WiFi Manager)

Type in the following

```md
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

If the file is already in that location you would see some text in it, if not you will get a new editor.

In that type int following:

```md
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
      ssid="CompanyName"
      proto=RSN
      key_mgmt=WPA-EAP
      pairwaie=CCMP
      aut_alg=OPEN
      eap=PEAP
      identity="user"
      password="123456"
}
```

Save it by doing <kbd class="uk-label">ctrl</kbd>+<kbd class="uk-label">X</kbd>, <kbd class="uk-label">return</kbd> and <kbd class="uk-label">return</kbd>.

Make sure you have connected your WiFi dongle. You should now be able to use the internet.
