---
title: 'Setting Up Powershell Core in Visual Studio Code for macOS'
date: 2018-12-03T10:30:16+05:30
draft: false
tags: ['PowerShell', 'macOS']
categories: ['Tutorial']
description: 'Setting up PowerShell Core for macOS is easy as making coffee on a coffee machine. Check this out.'
images: ["/img/blog/powershell-vscode-macos.jpg"]
ads: true
author:
  prefix: 'Mr.'
  firstName: 'Akshay Raj'
  lastName: 'Gollahalli'
  honorarySuffix: 'MCIS (FCH)'
  jobTitle: 'Research Assistant'
  email: 'akshay@gollahalli.com'
  addressCity: 'Hyderabad'
  addressCountry: 'India'
sitemap:
  priority: 0.8
  changeFreq: monthly
siteMapImages:
  - imageLoc: "/img/blog/powershell-vscode-macos.jpg"
    imageCaption: "PowerShell + macOS + VS Code = Heart"
---

{{< figure src="/img/blog/powershell-vscode-macos.jpg" alt="PowerShell + macOS + VS Code = Heart" title="PowerShell + macOS + VS Code = Heart" >}}

Things we need:

1. Apple computer/laptop running macOS 10.14 (yes, the expensive one)
2. Ruby (it's pre-installed on macOS, I have 2.3 pre-installed)
3. [Homebrew](https://brew.sh)
4. [Visual Studio Code](https://code.visualstudio.com/)
5. Patience to do this :)

If you are NOT a newbie, jump to [Step 4](#4-setting-up-vscode-to-use-powershell).

## 1. Installing Homebrew

Open `Terminal` and copy the link from the [Homebrew](https://brew.sh) website, this will install all the necessary packages and everything nice. Easy as.

## 2. Installing Visual Studio Code

Goto [Visual Studio Code](https://code.visualstudio.com/) website, click on the big, obvious, button to download the DMG package. Open the package and copy it to `Application` folder. Again, easy as.

## 3. Installing PowerShell Core

Open `Terminal` and type in

```md
brew cask install powershell
```

this should install the latest PowerShell Core, you can test it by typing in `pwsh` in your Terminal.

Tadaaaaa..!!

## 4. Setting up VSCode to use PowerShell

The easy way to set this up is by adding the code (below) to your `settings.json` file (remove the curly braces before adding). you can find this in <kbd class="uk-label">Command</kbd>+<kbd class="uk-label">,</kbd>.

```json
{
  "powershell.powerShellExePath": "/usr/local/microsoft/powershell/6/pwsh",
  "terminal.integrated.shell.osx": "/usr/local/bin/pwsh",
  "terminal.integrated.shellArgs.osx": []
}
```
> Note: `/usr/local/microsoft/powershell/6/pwsh` and `/usr/local/bin/pwsh` is the same.

By default, `"terminal.integrated.shellArgs.osx": []` has `"terminal.integrated.shellArgs.osx": ["-l"]`, this gives out error.