---
title: "git-alias: Over Engineered Pretty Git Alias Printer"
date: 2022-12-06T23:02:37+13:00
draft: false
categories: ["CLI"]
tags: ["Golang", "CLI Utility", "Git"]
description: ""
images: ["/img/blog/git-alias/git-alias-cover.gif", "/img/blog/git-alias/git-alias.png", "/img/blog/git-alias/git-alias-cover.png"]
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
  - imageLoc: "/img/blog/git-alias/git-alias-cover.gif"
    imageCaption: "Git Alias cover image"
  - imageLoc: "/img/blog/git-alias/git-alias-cover.png"
    imageCaption: "Git Alias cover image"
  - imageLoc: "/img/blog/git-alias/git-alias.png"
    imageCaption: "Git Alias"
---

> The binary files and the code can be found at [github.com/akshaybabloo/git-alias](https://github.com/akshaybabloo/git-alias).

Now there are different ways to list all the aliases in git. One of the ways is to use the command `git config --get-regexp alias` which will list all the aliases in the following format:

```bash
alias.la !git-alias
```

<!--adsense-->

But is it pretty, though? No. So, I decided to use Go language to make it look :heart_eyes:.

If you don't know Go language, it's a programming language developed by Google. It's a compiled language and it's pretty fast. It's also easy to learn. I would recommend you to learn it if you are interested in programming.

So, let's get started.

## The Binary File

The binary file is available for Windows, Linux and Mac. You can download it from the [releases](https://github.com/akshaybabloo/git-alias/releases) page or you can build it from the source code.

### The Usage

All you need to do is to download the binary file and place it in your `PATH` variable. Then you can use the command `git-alias` to list all the aliases.

```bash
$ git-alias
```

<!--adsense-->

This would list all the aliases in the following format:


```md
+---+-------+------------+
| # | ALIAS | COMMAND    |
+---+-------+------------+
| 1 | la    | !git-alias |
+---+-------+------------+
```

You can also search for a specific alias by using the `-s` flag.

```bash
$ git-alias -s la
```

This would list all the aliases which contains the string `alias` in the following format:

{{< figure src="/img/blog/git-alias/git-alias.png" title="Git Alias" alt="Git Alias" >}}

<!--adsense-->

### Adding it as a Git Alias

On your terminal, run the following command:

```bash
# This will work only if you have added the binary file to your PATH variable.
$ git config --global alias.la '!git-alias'
```

### Overriding the Default Git Config File Location

By default, the binary file will look for the `.gitconfig` file in the home directory. If you want to override the default location, you can use the `--config` flag.

```bash
$ git-alias --config "/path/to/.gitconfig"
```

## The Code

The code is pretty simple. It's just a single file. You can find the code [here](https://github.com/akshaybabloo/git-alias/blob/main/main.go).

I used the [gopkg.in/ini.v1](https://gopkg.in/ini.v1) package to parse the `.gitconfig` file. It's a simple package and it's easy to use.


```go
// ...
for _, key := range section.Keys() {
  if strings.Contains(key.Value(), SearchString) {
    valueIndex := strings.Index(key.Value(), SearchString)
    if valueIndex != -1 {
      t.AppendRow(table.Row{index, key.Name(), key.Value()[0:valueIndex] + c.Sprint(key.Value()[valueIndex:valueIndex+len(SearchString)]) + key.Value()[valueIndex+len(SearchString):]})
      t.AppendSeparator()
      index++
    }
  }
}
// ...

```

<!--adsense-->

The above code is used to list all the aliases. It is listed in a table format. The table is generated using the [github.com/jedib0t/go-pretty](https://github.com/jedib0t/go-pretty) package.

Happy Coding :heart:.


