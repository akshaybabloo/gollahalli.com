---
title: "Cookiecutter Template for Writing Go Command Line Interface"
date: 2021-06-27T18:25:31+12:00
draft: false
categories: ["Template"]
tags: ["Go", "cookiecutter"]
description: "A Go language template for building command line interface made easy by cookiecutter"
images: ["/img/blog/cookiecutter-template-for-writing-go-command-line-interface/cookiecutter-template-for-writing-go-command-line-interface.png"]
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
  - imageLoc: "/img/blog/cookiecutter-template-for-writing-go-command-line-interface/cookiecutter-template-for-writing-go-command-line-interface.png"
    imageCaption: "Cookiecutter Template for Writing Go Command Line Interface"
---

I have been developing a lot of Go language based CLIs and most of them have similar structure. And every time I start a new project I tend to rewrite the same structure. So, instead of doing that I copied the required code and turned in into a cookiecutter template :sunglasses:.

The repository is available at - [github.com/akshaybabloo/go-cli-template](https://github.com/akshaybabloo/go-cli-template).

> This template is highly inspired by [GitHub's CLI](https://github.com/cli/cli).

<!--adsense-->

## Requirements

1. Python 3.6+
   1. Install [cookiecutter](https://github.com/cookiecutter/cookiecutter)
2. Go 1.16+

## Usage

In your terminal type in

```sh
> cookiecutter https://github.com/akshaybabloo/go-cli-template
```

Then, follow the options on the terminal.

Once done, you will have to refactor the module path in `go.mod` to suit your project name, I usually have it as `github.com/akshaybabloo/<project-name>`.

## Features

1. Checks for updates once every 24 hours via GitHub API
2. Uses [Cobra](https://github.com/spf13/cobra) package for CLI
3. Factory based approach, functions are available on every command if needed
4. Global debug flag - uses [logrus](https://github.com/sirupsen/logrus)
5. Custom help output that also displays aliases
6. Uses custom color that's available via factory - uses [color](https://github.com/fatih/color)
7. Default global configuration location - `<user folder>/<project name>/config.yaml`
   1. Disable colour usage globally

<!--adsense-->

## Packages Used

Built using great open-source packages:

1. [heredoc](https://github.com/MakeNowJust/heredoc) - Package heredoc provides the here-document with keeping indent
2. [GitHub CLI](https://github.com/cli/cli) - GitHub command line tool package
3. [color](https://github.com/fatih/color) - Colour package
4. [uuid](https://github.com/google/uuid) - UUID generator
5. [go-version](https://github.com/hashicorp/go-version) - A library for parsing and verifying versions and version constraints 
6. [logrus](https://github.com/sirupsen/logrus) - Structured, pluggable logging for Go.
7. [afero](https://github.com/spf13/afero) - Afero is a filesystem framework providing a simple, uniform and universal API interacting with any filesystem
8. [Cobra](https://github.com/spf13/cobra) - Cobra is both a library for creating powerful modern CLI applications
9. [pflags](https://github.com/spf13/pflag) - pflag is a drop-in replacement for Go's flag package, implementing POSIX/GNU-style --flags
10. [testify](https://github.com/stretchr/testify) - A toolkit with common assertions and mocks that plays nicely with the standard library
11. [YAML v3](https://github.com/go-yaml/yaml/tree/v3) - YAML support for the Go language

## Conclusion

I hope this template is able to help you with your next project. Happy coding 😄.