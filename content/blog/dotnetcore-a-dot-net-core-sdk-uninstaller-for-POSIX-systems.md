---
title: "dotnetcore: A .Net Core SDK Uninstaller for POSIX Systems"
date: 2019-07-19T17:09:20+12:00
lastmod: 2019-09-07T14:33:10+12:00
draft: false
categories: ["CLI"]
tags: [".Net Core", "CLI", "Python"]
description: "There is no official way to remove previous versions of .Net Core SDKs in POSIX systems, this tool can help you with that."
images: ["/img/blog/dotnetcore.jpg"]
ads: true
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
  - imageLoc: "/img/blog/dotnetcore.jpg"
    imageCaption: "Uninstall previous versions of .Net Core SDK"
---

There is no official way to uninstall previous versions of .Net Core SDK on POSIX type operating systems, this tool may help you solve that problem.

> Note: This application only works on Linux type systems.

The repository can be found at [https://github.com/akshaybabloo/dot-net-core-uninstaller](https://github.com/akshaybabloo/dot-net-core-uninstaller).

> Note: You might need super user account to use this library.

## Instillation

```bash
pip install dot-net-core-uninstaller
```

## Usage

There are to ways to use this:

### Using Command Line Interface (recommended)

```bash
Usage: dotnetcore [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show version and exit.
  --help     Show this message and exit.

Commands:
  list    List all the version of .Net Core installed.
  remove  Remove the version of .Net Core.

```

To remove a version of .Net Core SDK or Runtimes:

```bash
> dotnetcore remove --sdk 1.0.0
> dotnetcore remove --runtime 1.0.0
```

To list all installed .Net Core libraries

```bash
> dotnetcore list
```

### Using as a Module

```python
from dot_net_core_uninstaller import Uninstaller

remove_dotnet = Uninstaller()
remove_dotnet.delete_runtime("1.0.0")
remove_dotnet.delete_sdk("1.0.0")
```
