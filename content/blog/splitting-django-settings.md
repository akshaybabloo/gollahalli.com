---
title: "Splitting Django Settings"
date: 2019-04-04T23:37:42+13:00
draft: true
tags: ["Python", "Azure", "Django"]
categories: ["Tips"]
description: ""
images: ["/img/blog/splitting_django_settings.png"]
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

{{< figure src="/img/blog/splitting_django_settings.png" alt="Splitting Django Settings" title="Splitting Django Settings" >}}

I have been working of few projects that uses django 2+ and deploying them to Azure Docker container. I do have one problem though, my development settings are very much different from my production. So, I split `settings.py` into a package with three extra files:

```md

```

## The .dockerignore file


## The \_\_init\_\_.py file


## The base.py file


## The local.py file


## The production.py file
