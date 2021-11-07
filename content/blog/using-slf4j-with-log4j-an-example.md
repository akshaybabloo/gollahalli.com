---
title: "Using SLF4J With Apache Log4j: An Example"
date: 2019-06-07T11:56:12+12:00
draft: false
categories: ["Tutorial"]
tags: ["Java"]
description: "A tutorial on using SLF4J with Apache Log4j in Java 8+."
images: ["/img/blog/slf4j-log4j.png"]
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
  - imageLoc: "/img/blog/slf4j-log4j.png"
    imageCaption: "A tutorial on using SLF4J with Apache Log4j in Java 8+"
---

Logging is essential when developing a software to keep a track on what is happening internally. This blog will show you how to use SLF4J with Apache Log4j.

<!-- TOC -->

- [1. Requirements](#1-requirements)
- [2. What is logging?](#2-what-is-logging)
  - [2.1. Logger](#21-logger)
    - [2.1.1. Name](#211-name)
    - [2.1.2. Levels](#212-levels)
  - [2.2. Pattern Layout](#22-pattern-layout)
  - [2.3. Appenders](#23-appenders)
    - [2.3.1. Console Appender](#231-console-appender)
    - [2.3.2. File with Pattern](#232-file-with-pattern)
    - [2.3.3. JSON File (Async)](#233-json-file-async)
- [3. What is Log4J?](#3-what-is-log4j)
  - [3.1. Why use Log4J when Java has java.util.logging?](#31-why-use-log4j-when-java-has-javautillogging)
- [4. What is SLF4J?](#4-what-is-slf4j)
  - [4.1. Why use SLF4J when Log4J has different types of log levels?](#41-why-use-slf4j-when-log4j-has-different-types-of-log-levels)
- [5. All about `log4j2.xml`](#5-all-about-log4j2xml)

<!-- /TOC -->

## 1. Requirements

This example assumes that you are familiar using Maven dependency manager. All the dependencies are listed in [pom.xml](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/pom.xml#L32-L67)

## 2. What is logging?

In general, logging refers to the recording of activity. In Java, logging can be divided into three levels:

```
            Logging
               |
  .------------+-------------.
  |            |             |
Logger      Formatter      Handler
                          (Appender)
```

### 2.1. Logger

Logger is an object, which is called when you want to log a message. Logger has two main objects in it:

- Name
- Logging levels

#### 2.1.1. Name

It is the class name of the application. For example `com.gollahalli.UsingLog4JSLF4J`. You can use this by calling

```java
logger.getName();
```

#### 2.1.2. Levels

They are the logging events that can be called while running a program.

Log4J and SLF4J provides the following levels of events:

|   Log4J  | SLF4J |
|:--------:|:-----:|
| ALL      | -     |
| DEBUG    | DEBUG |
| ERROR    | ERROR |
| FATAL    | -     |
| INFO     | INFO  |
| OFF      | -     |
| TRACE    | TRACE |
| WARN     | WARN  |
| CATCHING | -     |

### 2.2. Pattern Layout

For system output and file output, the pattern is the same. See [log4j2.xml#L6](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml#L6)

These are used to format the way the logs are displayed on the Terminal/Command Prompt or in the log files.

### 2.3. Appenders

In this example, there are three types of appenders

- Console
- File with Pattern (Async)
- JSON File (Async)

#### 2.3.1. Console Appender

This type of error writes the log event to the console using either of the two output methods

```Java
System.out
System.err
```

It defaults to `System.err`

See [log4j2.xml#L4-L7](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml#L4-L7)

#### 2.3.2. File with Pattern

`File` appenders are part of `AsyncAppender`, that means the file is written on a different thread. A simple file appender can have the same pattern as the console pattern but instead of showing it on the console its written to the file.

See [log4j2.xml#L9-L14](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml#L9-L14) - for file logging
See [log4j2.xml#L21-L24](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml#L21-L24) - for `Async` appender

#### 2.3.3. JSON File (Async)

Using additional libraries such as, `jackson` and `jackson-binding`, log events can be exported to JSON objects. Using `JsonLayout` under `File`, the file written is a JSON file.

See [log4j2.xml#L16-L19)](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml#L16-L19) - for JSON file logging
See [log4j2.xml#L21-L24](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml#L21-L24) - for `Async` appender

## 3. What is Log4J?

Log4J is a logging library for Java developed by Apache Logging project, which is a part of Apache Software Foundation Project.

### 3.1. Why use Log4J when Java has java.util.logging?

Apache can do everything that `java.util.logging` and more. Log4J can be used to log at the runtime. It also helps in lowering the performance cost. For more information see [Apache Logging](https://logging.apache.org/).

## 4. What is SLF4J?

Simple Logging Facade for Java (SLF4J) acts as an abstract layer for different types of logging libraries; this includes Log4J.

### 4.1. Why use SLF4J when Log4J has different types of log levels?

That's correct, but what if you don't want to use Log4J? And the person you give your code to has a different type of logger with them, that's when SLF4J comes in handy. For more information see [SLF4J](http://www.slf4j.org/).

## 5. All about `log4j2.xml`

There are three ways to configure Log4J. Using `XML`, `JSON` and `properties` file. For the purpose of this tutorial, we will stick to `XML`.

**Overview of Configuration File**

See [log4j2.xml](https://github.com/akshaybabloo/Using-Log4J-SLF4J/blob/master/src/main/resources/log4j2.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration ...>
    <Appenders>
        <!-- This is where your appenders go -->
    </Appenders>
    <Loggers>
        <Root ...>
          <!-- Refer to an appender from here -->
        </Root>
    </Loggers>
</Configuration>
```

For more information see [Log4J Configuration](https://logging.apache.org/log4j/2.x/manual/configuration.html).
