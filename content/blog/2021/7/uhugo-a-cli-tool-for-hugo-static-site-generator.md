---
title: "uHugo: A CLI Tool for Hugo Static Site Generator"
date: 2021-07-10T21:25:21+12:00
lastmod: 2023-06-26T21:25:21+12:00
draft: false
categories: ["CLI"]
tags: ["Python", "CLI Utility", "Hugo"]
description: "A CLI utility to download latest Hugo binary files, update it, and update cloud providers settings"
images: ["/img/blog/uhugo-a-cli-tool-for-hugo-static-site-generator/uHugo.png"]
ads: true
# htmlScripts: []
author:
  prefix: "Mr."
  firstName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Software Engineer"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
sitemap:
  priority: 0.8
  changeFreq: monthly
siteMapImages:
  - imageLoc: "/img/blog/uhugo-a-cli-tool-for-hugo-static-site-generator/uHugo.png"
    imageCaption: "uHugo: A CLI Tool for Hugo Static Site Generator"
---

[uHugo](https://github.com/akshaybabloo/uHugo) is a CLI utility tool written in Python for maintaining Hugo binary files. You might think "Wait! don't we have Homebrew, Chocolatey, Snap and a plethora of other tools for this?" that's exactly why, and also they are package managers. uHugo takes it to the next step by not only updating your Hugo binary file to the version you need, but also updates cloud provider's environment variables or configuration files. For example, [Cloudflare Pages](https://pages.cloudflare.com/) has a CI/CD system that builds and uploads the files to their storage place, but you will need to specify which version of Hugo you want to used to build these files. Some static host providers have configuration files to specify the version name, whereas Cloudflare Pages don't; you will need to specify the Hugo version under their environment variable section.

The process of updating environment variables can be automated via a CI/CD provider - GitHub actions, Travis, CircleCI etc. You name it using uHugo :star:.

Also, did I mention it is cross-platform CLI utility? :thinking:

<!--adsense-->

## How Should I Install It?

All you need is Python 3.6+ and its package manager - PIP. Open your terminal and type in:

```sh
> pip install uhugo
```

you can confirm the installation by typing:

```sh
> uhugo --version
```

## How Should I Use It?

Like any other package manager, it comes with two commands - `install` and `update`.

### Install Command

Installing a fresh Hugo binary is simple as:

```sh
> uhugo install
```

{{< figure src="/img/blog/uhugo-a-cli-tool-for-hugo-static-site-generator/uhugo-install.gif" title="uHugo instillation process" alt="uHugo instillation process" width="800" >}}

It does some basic steps:

- Checks if Hugo is installed 
- Gets the download URL of the latest binary from GitHub
- Downloads to a temporary folder
- Unzips it and move to `<user folder>/bin`, if the folder doesn't exist, it creates one for you

> Note: Make sure you have `<user folder>/bin` in your `$PATH`

There might be a time where you might want to reinstall the binary for this, you can use `--force` flag

```sh
> uhugo install --force
```

> Note: `--force` flag will only work when `<user folder>/bin` is in the `$PATH`

<!--adsense-->

### Update Command

Updating to the latest version of Hugo is simple as:

```sh
> uhugo update
```

{{< figure src="/img/blog/uhugo-a-cli-tool-for-hugo-static-site-generator/uhugo-update.gif" title="uHugo updating process" alt="uHugo updating process"  width="800" >}}

It takes the following steps to make you happy:

- Checks the local Hugo version
- Gets the latest Hugo version and compares it
- If the latest Hugo version is greater than the local Hugo version
  - Gets the download URL of the latest binary from GitHub
  - Downloads to a temporary folder
  - Unzips it and replaces `hugo` binary in `<user folder>/bin`

Update command can also be used to update any cloud provider's settings, though this is optional and this uHugo feature is unique from other CLI utilities. To activate this, few steps need to be taken:

1. Tell uHugo what providers you want it to check in Hugo's `config.toml` or `config.yaml`
2. Give your project name
3. Give an API key, if needed
4. Files to check or details regarding the provider

> Note: Above steps are only for Cloudflare Pages. For Netlify and Vercel, uHugo searches for `netlify.toml` and `vercel.json` respectively.

For example, I deploy my website on Cloudflare, so let's take an example of it. In my `config.toml`, I have the following settings:

```toml
[uhugo]
name = "cloudflare"
project = "gollahalli-com"
email_address = "env:email-address"
account_id = "env:account-id"
api_key = "env:api-key"
```

`env:email-account` is a special name in uHugo, this tells uHugo to replace the value `email-account` from the environment variable and use that value instead.

Whenever uHugo detects these configurations, it updates the value for `HUGO_VERSION` in production and preview environment variables.

<!--adsense-->

## Support for Cloud Providers

uHugo currently supports following cloud providers:

1. [Cloudflare](https://akshaybabloo.github.io/uHugo/providers/cloudflare.html) - API based
2. [Netlify](https://akshaybabloo.github.io/uHugo/providers/netlify.html) - File based, looks for `netlify.toml`
3. [Vercel](https://akshaybabloo.github.io/uHugo/providers/vercel.html) - File based, looks for `vercel.json`

## Final Thoughts

uHugo was purely built out of frustration for downloading the latest binary file and changing the variable names on Cloudflare (`login` > `use the correct account` > `Pages` > `select projects` > `settings tabs` > `environment variables tab` > `edit variables for production and preview` > `don't forget to save it` :tired_face:), Netlify (update the Hugo version in the config file) and Vercel.

I hope this CLI utility helps you in making your deployment a bit more productive.

Happy coding :nerd:
