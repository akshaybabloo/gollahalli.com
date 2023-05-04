---
title: "dnode: Search and Delete Node Modules Folders Recursively"
date: 2021-08-17T12:41:03+12:00
lastmod: 2023-05-04T14:33:10+12:00
draft: false
categories: ["CLI"]
tags: ["Golang", "CLI Utility"]
description: "Explore the power of dnode, a handy tool designed to help you efficiently search and delete Node Modules folders recursively. Save valuable disk space and declutter your development environment by mastering this essential utility for Node.js developers."
images: ["/img/blog/dnode-delete-node-modules-folders-recursively/dnode.png"]
ads: true
video: true
videos: ["/videos/blog/dnode-delete-node-modules-folders-recursively/dnode-list.mp4", "/videos/blog/dnode-delete-node-modules-folders-recursively/dnode-delete.mp4"]
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
  - imageLoc: "/img/blog/dnode-delete-node-modules-folders-recursively/dnode.png"
    imageCaption: "dnode: Search and Delete Node Modules Folders Recursively"
---

Source: [github.com/akshaybabloo/dnode](https://github.com/akshaybabloo/dnode)

Node's package managers makes it easy to develop applications, but the bloat it brings with it is (that's node_modules) painful. My 2013 Mac with 256 GB HDD cannot handle it. I currently have around eight projects that use `yarn` package manager and the total size of all `node_modules` comes to around **~2.2GB**. And lets not even get to the cache folder (Tip: `yarn cache clean`). All the hate for `node_modules` is totally justified.

All I want to do is to delete all unused `node_modules` folders (we all think that we will get back to it at some point but we never do), and there are different ways to do it:

1. Go to each project and delete the `node_modules` folder
2. Use one of the following shell scripts:
   1. Windows:
    ```sh
    FOR /d /r . %d in (node_modules) DO @IF EXIST "%d" rm -rf "%d"
    ```
   2. Linux:
    ```sh
    find . -name 'node_modules' -type d -prune -print -exec rm -rf '{}' \;
    ```
   3. PowerShell:
    ```ps1
    Get-ChildItem -Path "." -Include "node_modules" -Recurse -Directory | Remove-Item -Recurse -Force
    ```
3. Or use [dnode](https://github.com/akshaybabloo/dnode/releases/latest):
   ```sh
   dnode delete
   ```

## Instillation

There are pre-built binaries for Windows, macOS and Linux, these can be found at the [release](https://github.com/akshaybabloo/dnode/releases/latest) page.

Or you could build one yourself:

> Note: The code depends on Go 1.17 or above

```sh
git clone https://github.com/akshaybabloo/dnode.git
cd dnode
go build -o dnode
./dnode --help
```

<!--adsense-->

## Usage

There are two commands - `list` and `delete`.

### List

`dnode list` lists all the unused `node_modules` folders in the current directory tree.
 
 Example:

{{< video src="/videos/blog/dnode-delete-node-modules-folders-recursively/dnode-list" >}}

### Delete

`dnode delete` deletes all the unused `node_modules` folders in the current directory tree.

 Example:

{{< video src="/videos/blog/dnode-delete-node-modules-folders-recursively/dnode-delete" >}}

## Final Thoughts

Again, this CLI was developed out of frustration to get rid of unused `node_modules` folders. I hope you find it useful.

Happy coding 🍾
