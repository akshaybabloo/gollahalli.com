---
title: "Stopping HTTP Server Gracefully: Context vs Channels vs SyncGroup"
date: 2020-02-02T13:01:03+13:00
draft: false
categories: ["Tutorial"]
tags: ["Go"]
description: ""
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

> Full code can be found at [github.com/akshaybabloo/gracefully-exit-go-http-server](https://github.com/akshaybabloo/gracefully-exit-go-http-server)

I am developing a CLI application that requires it to authenticate and obtain a token from an API. I had a problem of gracefully shutting down the the HTTP server from another function, in this case, after a token is received.

In this post we will look at using three ways to tell the server to shut down gracefully. Also, I am using Gorilla's mux router.

Before we go into the details, there are few common functions between these three implementations:

1. There are two handles (routes); `HomeHandler` - that routes to `127.0.0.1:8000/`, which is our index page and `ExitHandler` - that routes to `127.0.0.1:8000/exit`, which is used to shut down the server.
2. The server always starts in a gorutine.
3. The program doesn't exit till some kind of wait request is completed.

- [Using with Channels](#using-with-channels)
- [Using with Context](#using-with-context)
- [Using with WaitGroup](#using-with-waitgroup)

## Using with Channels

Channels are like pathways, it joins gorutines to send and receive messages. For example:

See [play.golang.org/p/BC3IBnNjzb5](https://play.golang.org/p/BC3IBnNjzb5)

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	message := make(chan string)

	go func() {
		fmt.Println("Hello from gorutine")
		time.Sleep(2 * time.Second) // wait for two seconds
		message <- "Hello World!"
	}()

	receivedMessage := <-message
	fmt.Println(receivedMessage)
	// Hello World!
}
```

In the above example we created a channel called `message`, an anonymous gorutine is run and a text is sent to the `message` channel. The channel doesn't let the program end unless a message is received at `receivedMessage`. Once the message is received, the text is assigned to `receivedMessage`, then prints it out and eventually exits the program.

Using the channels let's see how we can shut down the serve from a different handle:

```go {linenos=table,hl_lines=[13,30,34,58]}
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

var stopHTTPServerChan chan bool

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, err := fmt.Fprintln(w, "<h1>Home of Channels</h1><br><a href='/exit'>Exit</a>")
	if err != nil {
		panic(err)
	}
}

func ExitHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, err := fmt.Fprintln(w, "<h1>Bye from Channels</h1>")
	if err != nil {
		panic(err)
	}
	// sends a signal to the channel, this could even be false it doesn't matter
	stopHTTPServerChan <- true
}

func StartServer() {
	stopHTTPServerChan = make(chan bool)
	r := mux.NewRouter()
	r.HandleFunc("/", HomeHandler)
	r.HandleFunc("/exit", ExitHandler)

	fmt.Println("Server started at http://127.0.0.1:8000")

	srv := &http.Server{
		Handler: r,
		Addr:    "127.0.0.1:8000",
		// Good practice: enforce timeouts for servers you create!
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	go func() {
		// always returns error. ErrServerClosed on graceful close
		if err := srv.ListenAndServe(); err != http.ErrServerClosed {
			// unexpected error. port in use?
			log.Fatalf("ListenAndServe(): %v", err)
		}
	}()

	// wait here till a signal is received
	<-stopHTTPServerChan
	if err := srv.Shutdown(context.TODO()); err != nil {
		panic(err) // failure/timeout shutting down the server gracefully
	}
	fmt.Println("Server closed - Channels")
}
```

In the above example, we have a global channel `stopHTTPServerChan` (line 13) of type `bool`. In the `main()` function, let's a make a channel that has a type of `bool` and assign it to our global variable `stopHTTPServerChan` (line 34). When the server starts it won't end abruptly, because of `<-stopHTTPServerChan` (line 58), the program waits here till a boolean signal is received. Under `ExitHandler()` send a signal a boolean signal as `stopHTTPServerChan <- true` (line 30, this could also be `false`), so whenever you go to `http://127.0.0.1:8000/exit` a signal is sent to `stopHTTPServerChan`, once the boolean value is received, the wait is over then it proceeds to the next line.

## Using with Context

```go

```

## Using with WaitGroup

```go

```
