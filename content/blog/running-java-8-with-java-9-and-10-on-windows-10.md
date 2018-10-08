---
title: "Running Java 8 With Java 9 and 10 on Windows 10"
date: 2018-04-04T14:33:10+12:00
draft: false
categories: ["Tutorial"]
tags: ["Java"]
description: "Java 9+ and problems with it's path."
images: ["/img/blog/java_path.jpg", "/img/blog/edit_string.JPG", "/img/blog/regedit.JPG"]
ads: true
author:
  prefix: "Mr."
  fistName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Research Assistant"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
siteMapImages:
  - imageLoc: "/img/blog/java_path.jpg"
    imageCaption: "Running different version of java"
  - imageLoc: "/img/blog/edit_string.JPG"
    imageCaption: "Registry Editor"
  - imageLoc: "/img/blog/regedit.JPG"
    imageCaption: "Registry Editor"
sitemap:
  priority: 0.8
  changeFreq: monthly
---

{{< figure src="/img/blog/java_path.jpg" alt="Running different version of java" >}}

Oracle has decided that from Java 9 there will be a new java version every six months and the third release would be an LTS release (?). More on it [here](https://medium.com/codefx-weekly/radical-new-plans-for-java-5f237ab05b0).

Not all libraries have upgraded them self to the latest Java releases, for example at the time of writing this Scala 2.12.5 doesn't fully support Java 9, so I still had to use Java 8. For some reason, if you want to experiment with the newer releases of Java and for the same reason, if you install Java 9 or 10, you just cannot run Scala (or other libraries that run Java 8) that's because Java 9/10 changes your path. Even though you add a **JAVA_HOME** variable, you still find Java 9/10 being used in command line.

## How did this happen?

When you installed Java 9 or 10 via the **exe** file, a default path variable was registered in the windows registry:

{{< figure src="/img/blog/regedit.JPG" title="Registry Editor" alt="Registry Editor" >}}

* From the start menu, open Run (or press Win+R).
* Type **regedit**
  * Find **HKEY_LOCAL_MACHINE** folder
  * Go to the **SYSTEM** folder
  * Go to the **ControlSet001** folder (you might have a different ControlSet number)
  * Go to **Control** folder
  * Go to **Session Manager**
  * Go to **Environment** folder
  * Then, inside **Environment** folder, see Path (you can double and delete the path if you want to)

Complete path: **Computer\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment**

The first location in the **Path** is where the new Java versions are stored. When you open a new command line (cmd.exe) the first thing it does it to load the default paths mentioned in the **Registry Editor** (above) and then loads the user paths, so the newer Java supersedes the old ones.

You can check this by opening your command line and enter **java -version**, you should see:

```md
java version "10" 2018-03-20
Java(TM) SE Runtime Environment 18.3 (build 10+46)
Java HotSpot(TM) 64-Bit Server VM 18.3 (build 10+46, mixed mode)
Even though you have JAVA_HOME environment variable, you will see the newer ones, as I said earlier, defaults paths are loaded first.
```

You can test this by doing where java your output will be something like this:

```md
C:\ProgramData\Oracle\Java\javapath\java.exe
C:\Program Files\Java\jre1.8.0_162\bin\java.exe
```

## So how to fix this?

There are two way to do this:

### FIX 1

You can delete the path - **C:\ProgramData\Oracle\Java\javapath** from the default **Path** mentioned in **Registry Editor**. You will need to double-click on the Path, which will open:

{{< figure src="/img/blog/edit_string.JPG" title="Registry Editor" alt="Registry Editor" >}}

Once you have removed the path, close and reopen your command prompt, if you have **JAVA_HOME** for Java 8 you should be able to run (for me) Scala.

### FIX 2

Another way is to go to **C:\ProgramData\Oracle\Java** and delete javapath (you will not lose any data because this is a shortcut to javapath-*)

If you don't have **JAVA_HOME** for Java 8, do the following:

Open your command prompt and type in:

```md
> setx JAVA_HOME "C:\Program Files\Java\jre1.8.0_162"
> setx PATH "%PATH%;%JAVA_HOME%\bin"
```

This will update your user environment variables.

## But how to use Java 9 or Java 10?

Again, there are two ways:

### WAY 1

You can change the JAVA_HOME path to Java 9 or Java 10 from your command prompt:

For Java 9:

```md
> setx JAVA_HOME "C:\Program Files\Java\jdk-9.0.4"
```

For Java 10:

```md
> setx JAVA_HOME "C:\Program Files\Java\jdk-10"
```

### WAY 2

You can add a temporary path to your command prompt's current session by doing:

For Java 9:

```md
> set JAVA_HOME=C:\Program Files\Java\jdk-9.0.4
> set PATH=%PATH%;%JAVA_HOME%\bin
```

For Java 10:

```md
> set JAVA_HOME=C:\Program Files\Java\jdk-10
> set PATH=%PATH%;%JAVA_HOME%\bin
```

Happy coding!

---

**Update 27/06/2018:**

Path to the registry editor added.