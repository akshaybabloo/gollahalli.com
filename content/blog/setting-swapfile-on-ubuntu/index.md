---
title: "Setting Swapfile on Ubuntu"
date: 2024-05-08T13:26:07+12:00
draft: false
categories: ["Linux"]
tags: ["ubuntu", "swapfile", "linux"]
description: "Is your system running out of memory? Here is how you can set up a swap file on Ubuntu."
images: ["swapfile-blog.png"]
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
siteMapImages:
  - imageLoc: "swapfile-blog.png"
    imageCaption: "Setting Swapfile on Ubuntu"
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

open a terminal and follow the steps below:


List the current swap file

```bash
sudo swapon --show

# NAME      TYPE SIZE USED PRIO
# /dev/dm-1 file  20G   0B   -2
```

Switch off the running swap file (this will take a while depending on the file size)

```bash
sudo swapoff /dev/dm-1
```

Create a new file with required file size, here is an example of one with 16 GB

```bash
sudo fallocate -l 16G /swapfile
```

Change the access permissions so that only root can access it

```bash
sudo chmod 0600 /swapfile
```

Set this as the swap space

```bash
sudo mkswap /swapfile
```

Activate the swap space

```bash
sudo swapon /swapfile
```

You can confirm if by typing

```bash
sudo swapon --show

# NAME      TYPE SIZE USED PRIO
# /swapfile file  20G   0B   -2
```

Make it persistent, so that the swap file is mounted automatically on system boot. There are two ways to do this:

```bash
# Create a backup of the fstab
sudo cp /etc/fstab /etc/fstab.bak

# Edit the fstab file
sudo nano /etc/fstab

# Add the following line at the end of the file
/swapfile       swap            swap    defaults          0     0
```

**_OR_**

Instead of using `nano`, you can use the following command to append the line to the end of the file:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## Conclusion

That's it! You have successfully set up a swap file on your Ubuntu system. If you have any questions or face any issues, feel free to leave a comment below.