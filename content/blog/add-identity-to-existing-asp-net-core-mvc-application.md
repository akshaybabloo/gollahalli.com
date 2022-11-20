---
title: "Add Identity to Existing Asp.Net Core MVC Application"
date: 2020-03-24T09:45:24+13:00
draft: true
categories: []
tags: []
description: "A tutorial on how to add authentication to an existing Asp.Net Core MVC application"
images: []
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
# siteMapImages:
#   - imageLoc: ""
#     imageCaption: ""
---

## Create a New Project
For this example, let's create a new project called `IdentityExample` using the dotnet CLI:

`dotnet new mvc -o IdentityExample`

### Adding the Required Libraries

Identity depends on few libraries and to make our lives easy we will use the trust Entity framework which does all the database work for use. Using the `dotnet` CLI, do the following:

In your terminal:

1. `dotnet add package Microsoft.AspNetCore.Identity.EntityFrameworkCore` - ASP.NET core identity support
2. `dotnet add package Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore` - Diagnose EF errors
3. `dotnet add package Microsoft.AspNetCore.Identity.UI` - Razor page support
4. `dotnet add package Microsoft.EntityFrameworkCore.Sqlite` - Support for SqLite database
5. `dotnet add package Microsoft.EntityFrameworkCore.Tools` - Support for `ef` CLI

### Setup SqlLite Credentials

In `appsettings.json` add:

```json {linenos=table,hl_lines=[2,3,4]}
{
  "ConnectionStrings": {
    "DefaultConnection": "DataSource=app.db"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "AllowedHosts": "*"
}
```
<!--adsense-->

### Adding DB Context

`AccountDbContext.cs` - See 

Create a folder `Data` under `IdentityExample`. In that create `AccountDbContext.cs`.

Now, in `Startup.cs`, under `ConfigureServices`, write in the highlighted code:

```cs {linenos=table,hl_lines=[4,5]}
public void ConfigureServices(IServiceCollection services)
{

  services.AddDbContext<AccountDbContext>(options => options.UseSqlite(_configuration.GetConnectionString("DefaultConnection")));
  services.AddDefaultIdentity<IdentityUser>(options => options.SignIn.RequireConfirmedAccount = true).AddEntityFrameworkStores<AccountDbContext>();

  services.AddControllersWithViews();
}
```

#### Create Migrations and Update Database

Using the `dotnet` CLI let's create the migrations for `AccountDbContext`. In your terminal type in - `dotnet ef migrations add Account`. Once the migrations have been generated, let's the push it to the database by doing - `dotnet ef database update`.

### Configure ASP.NET Core to use Identity

After creating the migrations, we need to tell the application to used authentication. To do that, under `Configure` method in `Startup.cs`, add the following code:

```cs {linenos=table,hl_lines=[10]}
public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
{
  //...

  app.UseHttpsRedirection();
  app.UseStaticFiles();

  app.UseRouting();

  app.UseAuthentication();
  app.UseAuthorization();

  //...
}
```

<!--adsense-->

### Adding the Controllers and Views

Identity comes with preconfigured database context, to enable that, do the following:

1. Create a new folder under

Create three controllers with their views as:

1. `Account/LoginController.cs` and `Login/Index.cshtml` - This will be used to authenticate the user
2. `Account/LogoutController.cs` and `Logout/Index.cshtml` - This will be used to logout the users session
3. `Account/RegisterController.cs` and `Register/Index.cshtml` - This will be used to create a user
4. `Account/ConfirmRegisterController.cs` and `ConfirmRegister/Index.cshtml` - This will be used to create a user

### Creating the Account Models
