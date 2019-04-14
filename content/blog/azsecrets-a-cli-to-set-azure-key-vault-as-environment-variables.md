---
title: "azsecrets: A CLI to Set Azure Key Vault as Environment Variables"
date: 2019-04-13T18:05:05+12:00
draft: false
categories: ["CLI"]
tags: ["Python", "Azure", "CLI"]
description: "Use Azure Key Vault to set your environment variable using 'azsecrets' CLI tool."
images: ["/img/blog/azsecrets.jpg"]
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
siteMapImages:
  - imageLoc: "/img/blog/azsecrets.jpg"
    imageCaption: "azsecrets: A Cli to Set Azure Key Vault as Environment Variables"
---

**Repository: [https://github.com/akshaybabloo/azure-keyvault-secret-env](https://github.com/akshaybabloo/azure-keyvault-secret-env)**
**Documentation: [https://akshaybabloo.github.io/azure-keyvault-secret-env/](https://akshaybabloo.github.io/azure-keyvault-secret-env/)**

Using environment variables to store your secrets is one of the more natural way to do; these variables then can be used in your code throughout the life cycle of your Docker environment. You shouldn't hard code your secret keys inside your application; it is just not secured. Docker lets you add the environment variable before creating an image or at the entry point when starting up your image, `azsecrets` lets you set these environment variables that are stored in Azure Key Vault.

I have borrowed the idea from `docker-machine env` CLI command, that spits out several environment variables that it needs to connect Docker CLI to a virtual machine; `azsecrets` does that for you.

This package can also be used as a module in your current code if you don't want to use it as a CLI.

## Instillation

The CLI is written in Python 3 and is available in PyPi at [https://pypi.org/project/azsecrets/](https://pypi.org/project/azsecrets/). To install it open your CMD/Terminal/Powershell and type in

```cmd
pip install azsecrets
```

## Usage

There are two ways to use `azsecrets`: as a CLI or as a package

### Command Line Interface

Once you have installed the tool, you will have to set four environment variables (or give it as an argument in CLI) that Azure uses to access Key Vault.

```cmd
AZURE_VAULT_BASE_URL=***
AZURE_CLIENT_ID=***
AZURE_SECRET_KEY=***
AZURE_TENANT_ID=***
```

You can then open CMD/Terminal/Powershell and type in

```bash
secrets env --shell bash
# export VAR-1=secret1
# export VAR-2=secret2
```

or via CLI

```bash
secrets --vault-base-url *** --client-id *** --secret *** --tenant *** env --shell bash
# export VAR-1=secret1
# export VAR-2=secret2
```

`secrets --help` will give you more information on the usage.

```cmd
(base) akshayrajgollahalli:~ : secrets --help
Usage: secrets [OPTIONS] COMMAND [ARGS]...

Options:
  --version              Show version and exit.
  --vault-base-url TEXT  Azure KeyVault base URL. Defaults to None.
  --client-id TEXT       Azure KeyVault client ID.
  --secret TEXT          Azure KeyVault secret.
  --tenant TEXT          Azure tenant ID.
  --help                 Show this message and exit.

Commands:
  env  Environment configuration: [powershell, cmd or bash].
```

### As a Package

You can also use `azsecrets` as a package by just importing the object to your existing Python code; for example, in Django, you can set your secrets by doing (this example assumes that you have already set the four environment variables):

```python
from azsecrets import AzureSecrets

# You can also set the four environment variables or pass the arguments through the object
az_secrets = AzureSecrets()

SECRET_KEY = az_secrets.get_secret("DJANGO-SECRET-KEY")
```

See [https://akshaybabloo.github.io/azure-keyvault-secret-env/](https://akshaybabloo.github.io/azure-keyvault-secret-env/) for more information.

Happy coding.
