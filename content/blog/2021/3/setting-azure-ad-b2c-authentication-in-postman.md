---
title: "Setting Azure AD B2C Authentication in Postman"
date: 2021-03-04T16:20:34+13:00
draft: false
categories: ["Azure"]
tags: ["OAuth2", "Azure AD B2C", "postman"]
description: "Using Azure AD B2C in development with Postman"
images: ["/img/blog/setting-azure-ad-b2c-authentication-in-postman/b2c-banner.png", "/img/blog/setting-azure-ad-b2c-authentication-in-postman/add-platform.png", "/img/blog/setting-azure-ad-b2c-authentication-in-postman/callback-url.png", "/img/blog/setting-azure-ad-b2c-authentication-in-postman/grants.png", "/img/blog/setting-azure-ad-b2c-authentication-in-postman/postman.png"]
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
  - imageLoc: "/img/blog/setting-azure-ad-b2c-authentication-in-postman/b2c-banner.png"
    imageCaption: "Setting Azure AD B2C Authentication in Postman"
  - imageLoc: "/img/blog/setting-azure-ad-b2c-authentication-in-postman/add-platform.png"
    imageCaption: "Add a new platform"
  - imageLoc: "/img/blog/setting-azure-ad-b2c-authentication-in-postman/callback-url.png"
    imageCaption: "Adding callback URL"
  - imageLoc: "/img/blog/setting-azure-ad-b2c-authentication-in-postman/grants.png"
    imageCaption: "Enable grants"
  - imageLoc: "/img/blog/setting-azure-ad-b2c-authentication-in-postman/postman.png"
    imageCaption: "Screenshot of Postman authentication setup"
---

Azure AD B2C has been so far good, mostly because of the 50k free user authentication :innocent:, also it just works. The problem I had using B2C with backend was acquiring and testing tokens in development.

Yes, Azure AD B2C has Resource Owner Password Credential (ROPC) flow that allows you to get tokens by just posting your username and password, but [they don't recommend it](https://docs.microsoft.com/en-us/azure/active-directory/develop/msal-net-aad-b2c-considerations#resource-owner-password-credentials-ropc). Though, I have been using that locally to get the tokens.

With the new update of Postman (version 8+), its easy to set OAuth 2.0 based authentication.

So, lets set it up.

## Setup Azure AD B2C

> Note: This article assumes that you have basic knowledge about OAuth 2.0 and Azure AD B2C

Before we get the tokens, we should tell Azure AD B2C that we want to authenticate using Authorisation code flow with [Proof Key for Code Exchanged (PKCE)](https://tools.ietf.org/html/rfc7636).

At the time of writing this article, Azure AD B2C supports the following platforms:

1. Web applications
   1. Web
   2. Single-page application
2. Mobile and desktop application
   1. iOS/macOS
   2. Android
   3. Mobile and desktop application

For web applications you need client security code because as far as I have tested it, it doesn't work with PKCE. I chose - Mobile and desktop application - because Postman is a desktop application. Let's add a platform first:

1. In Azure AD B2C directory, select - `App registrations` - from the left menu
2. Under `Owned applications` tab, select your application.
3. From the left menu, under `Manage` section, select `Authentication`
4. Under - Platform configurations - click on `Add a platform`. This should open a drawer from right.
    {{< figure src="/img/blog/setting-azure-ad-b2c-authentication-in-postman/add-platform.png" title="Add a new platform" alt="Add a new platform" class="uk-align-center" >}}
    select the - Mobile and desktop applications.
5. According to their [documentation](https://learning.postman.com/docs/sending-requests/authorization/#requesting-an-oauth-20-token), the callback URL should be - `https://www.postman.com/oauth2/callback`, add that and click `Configure`.
    {{< figure src="/img/blog/setting-azure-ad-b2c-authentication-in-postman/callback-url.png" title="Adding callback URL" alt="Adding callback URL" class="uk-align-center" >}}
    This will create the appropriate platform.
6. Also, in the same page, under `Implicit grant and hybrid flows`, make sure `Access tokens` and `ID tokens` are ticked.
    {{< figure src="/img/blog/setting-azure-ad-b2c-authentication-in-postman/grants.png" title="Enable grants" alt="Enable grants" class="uk-align-center" >}}

## Setup Postman

At this point make sure you know your endpoints for - `authorize` and `token`, mine is:

- Authorize - https://gollahalliauth.b2clogin.com/gollahalliauth.onmicrosoft.com/B2C_1_SignUpSignInFlow/oauth2/v2.0/authorize
- Token - https://gollahalliauth.b2clogin.com/gollahalliauth.onmicrosoft.com/B2C_1_SignUpSignInFlow/oauth2/v2.0/token

Lets setup Oauth 2.0:

Go to collection setting, click on `Authorization` tab and do the following:

{{< table "uk-table uk-table-small uk-table-responsive" >}}
| Type             | Entry          | Description |
| ---------------- | -------------- | ----------- |
| Type             | OAuth 2.0      | Type of authentication |
| Add auth data to | Request Header | Once an `access_token` is received, where do you want it to be placed|
{{</ table>}}

### Configure New Token

{{< table "uk-table uk-table-small uk-table-expand" >}}
| Type                    | Entry                                                                                                                                                     | Description                                                           |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Type Name               | Azure AD B2C Authentication                                                                                                                               | This is up to you                                                     |
| Grant Type              | Authorization Code (With PKCE)                                                                                                                            |                                                                       |
| Callback URL            | https://www.postman.com/oauth2/callback                                                                                                                   | This cannot be edited                                                 |
| Authorize using browser | Tick                                                                                                                                                      |                                                                       |
| Auth URL                | https://gollahalliauth.b2clogin.com/gollahalliauth.onmicrosoft.com/B2C_1_SignUpSignInFlow/oauth2/v2.0/authorize?nonce={{$randomUUID}}&response_mode=query | `$randomUUID` generate a UUID V4 and the response should be URL query |
| Access Token URL        | https://gollahalliauth.b2clogin.com/gollahalliauth.onmicrosoft.com/B2C_1_SignUpSignInFlow/oauth2/v2.0/token                                               |                                                                       |
| Client ID               | \<your client ID\>                                                                                                                                          |                                                                       |
| Client Secret           |                                                                                                                                                           | This should be empty                                                  |
| Code Challenge Method   | SHA-256                                                                                                                                                   |                                                                       |
| Code Verifier           |                                                                                                                                                           | This should be empty so that Postman can generate one for you         |
| Scope                   | \<custom scope\> openid profile offline_access                                                                                                              |                                                                       |
| State                   | {{$randomUUID}}                                                                                                                                           | `$randomUUID` generate a UUID V4                                      |
| Client Authentication   | Send client credentials in body                                                                                                                           |                                                                       |
{{</ table>}}

#### Screenshot

{{< figure src="/img/blog/setting-azure-ad-b2c-authentication-in-postman/postman.png" title="Screenshot of Postman authentication setup" alt="Screenshot of Postman authentication setup" class="uk-align-center" width="600" >}}

## Conclusion

These steps should be similar to other OAuth providers. Do give it a try and let me know if there is a space for improvements. I hope this article helps you in your development.
