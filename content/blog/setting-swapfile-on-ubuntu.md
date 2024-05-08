---
title: "Setting Swapfile on Ubuntu"
date: 2024-05-08T13:26:07+12:00
draft: false
categories: []
tags: []
description: ""
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
# siteMapVideos:
#   - videoLoc: ""
#     videoDescription: ""
---

<!--adsense-->

When you are running out of memory on your Linux system, the OS starts killing processes to free up the memory. This is not a good idea, as it can lead to data loss. To avoid this, a swap file is used. By default, Ubuntu creates a swap file during installation. However, if you want to create a new swap file or change the size of the existing swap file, you can do so by following the steps below.

### How to check if a swap file is already present?

To check if a swap file is already present, run the following command:

```bash
sudo swapon --show
```

You should see the swap file listed if it is present. On my system, the output is as follows:

```md
NAME      TYPE      SIZE USED PRIO
/dev/dm-2 partition 1.9G   0B   -2
```

Ubuntu has stopped using swap partitions and has started using swap files. But for me, the swap file is not listed instead a swap partition is listed - `/dev/dm-2`.

## How to set it up then?
