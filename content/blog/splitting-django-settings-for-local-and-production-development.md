---
title: "Splitting Django Settings for Local and Production Development"
date: 2019-04-04T23:37:42+13:00
draft: false
tags: ["Python", "Azure", "Django"]
categories: ["Tips"]
description: "Sometimes you don't want to use the settings for your production in a local environment and vice versa, this blog will help you with it."
images: ["/img/blog/splitting_django_settings.png"]
ads: true
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
  - imageLoc: "/img/blog/splitting_django_settings.png"
    imageCaption: "Splitting Django Settings for Local and Production Development"
---

I have been working on a few projects that use Django 2+ and deploying them to Azure Docker container. I do have one problem though; my development settings are very much different from my production. So, I  have divided `settings.py` into a package with - `base.py`, `local.py` and `production.py`:

```tree
<project name>
├── <project name>
│   ├── __init__.py
│   └── settings
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       └── production.py
└── .dockerignore
```

<!--adsense-->

## `.dockerignore` file

While building a container, the CLI looks for `.dockerignore` file, which contains the file or file pattern to be ignored before sending the information to the Docker daemon. We can compare this to `.gitignore`, that ignores any file mentioned in this before committing into the version control.

This file ignores `local.py`.

You can learn more about it at their website -> [https://docs.docker.com/engine/reference/builder/#dockerignore-file](https://docs.docker.com/engine/reference/builder/#dockerignore-file).

## `__init__.py` file

Here, we check for `local.py`, if it exists this is imported and if not, `production.py` is used.

```python
from .base import *

try:
    from .local import *

    live = False
except ImportError:
    live = True

if live:
    from .production import *
```

<!--adsense-->

## `base.py` file

This is the base for both local and production, the common code. Now it depends if you want to use the same `SECRET_KEY` on both production and local, I use it in both ways. If it's a commercial project, I separate it and if not I put it in the `base.py`. Also, if you are using external logging providers such as Logstash or Sentry, you might want to separate `LOGGING` too.

The common code I use is:

```python
BASE_DIR = ******
# This depends on you.
SECRET_KEY = ******

INSTALLED_APPS = [
    ...
]
MIDDLEWARE = [
    ...
]
ROOT_URLCONF = '******'
TEMPLATES = [
    ...
]
WSGI_APPLICATION = '******'
AUTH_PASSWORD_VALIDATORS = [
    ...
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGGING = {
    ...
}
EMAIL_HOST = ******
EMAIL_PORT = ******
EMAIL_USE_SSL = ******
EMAIL_HOST_USER = ******
EMAIL_HOST_PASSWORD = ******
```

<!--adsense-->

## `local.py` file

I always separate my database, and I also make sure that they are the same type of database, in my case it's PostgreSQL. Also, it contains the location for the static file and where the user can upload their files.

Code:

```python
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    ...
}

SHARE_URL = "http://127.0.0.1:8000"

# Static assets
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static_dirs'),
)

# User uploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
```

<!--adsense-->

## `production.py` file

This is where I use external services such as Azure, AWS or Heroku to add their production settings. I also restrict the access to one domain, disable `DEBUG`, use `whitenoise` for static assets and use `dj_database_url` for parsing PostgreSQL URL.

The code:

```python
DEBUG = False

ALLOWED_HOSTS = ['******']

# Database connection to Azure URL
DATABASES = settings.DATABASES
DATABASES['default'] = dj_database_url.parse('******', conn_max_age=500,
                                             ssl_require=True)
# For django storages
AZURE_ACCOUNT_NAME = ******
AZURE_ACCOUNT_KEY = ******
AZURE_CONTAINER = ******

SHARE_URL = "******"

AZURE_BLOB_CUSTOM_DOMAIN = '******'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = '******'
STATIC_URL = "https://%s/%s/" % (AZURE_BLOB_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = '******'
MEDIA_URL = "https://%s/%s/" % (AZURE_BLOB_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
```

<!--adsense-->

## Finally

One last tip is that I use my secrets as an environment variable or use the Azure Key Vault; this gives extra security and flexibility.

Happy coding.