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

I am developing a CLI application that requires it to authenticate and obtain a token from an API. I had a problem of gracefully shutting down the the HTTP server from another function, in this case, after a token is received. Go 1.8 introduced `Shutdown` that gracefully shuts down the server without interrupting any active connections.

In this post we will look at using three ways to tell the server to shut down gracefully. Also, I am using Gorilla's mux router.

Before we go into the details, there are few common functions between these three implementations:

1. There are two handles (routes); `HomeHandler` - that routes to `127.0.0.1:8000/`, which is our index page and `ExitHandler` - that routes to `127.0.0.1:8000/exit`, which is used to shut down the server.
2. The server always starts in a goroutine.
3. The program doesn't exit till some kind of wait request is completed.

**Table of Content**

- [Using with Channels](#using-with-channels)
- [Using with Context](#using-with-context)
- [Using with WaitGroup](#using-with-waitgroup)
- [Conclusion](#conclusion)

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

> Note: According to the documentations, contexts should never be stored in `struct` type but rather it should be passed through with few exceptions; `context.CancelFunc` is one such exception.

Contexts in the backend uses channels to send and receive messages but in a server scenario, every request received runs on a gorutine. Some requests might take more time than required, for fewer request the server should usually be able to handel them without using too much resources, but when there are 1000's of request per-second the system might crash, the context library comes with function, such as - WithCancel, WithDeadline, WithTimeout, and WithValue - that helps in destroying a request if it takes time that is allocated to it.

See [play.golang.org/p/3scpKiCypIS](https://play.golang.org/p/3scpKiCypIS)

```go
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())

	go func() {
		fmt.Println("Hello from gorutine")
		time.Sleep(2 * time.Second) // wait for two seconds
		cancel()
	}()

	<-ctx.Done()
	fmt.Println("Hello World!")
	// Hello World!
}
```

Above example works exactly like channels example, only that you don't have to make a channel and looks pretty.

```go {linenos=table,hl_lines=["13-15",32,"36-37","61-62"]}
package withcontext

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type httpServerHelper struct {
	cancelFunc context.CancelFunc
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, err := fmt.Fprintln(w, "<h1>Home of Context</h1><br><a href='/exit'>Exit</a>")
	if err != nil {
		panic(err)
	}
}

func (helper *httpServerHelper) ExitHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, err := fmt.Fprintln(w, "<h1>Bye from Context</h1>")
	if err != nil {
		panic(err)
	}
	// Execute a cancel function
	helper.cancelFunc()
}

func main() {
	stopHTTPServerCtx, cancel := context.WithCancel(context.Background())
	serverHelper := &httpServerHelper{cancelFunc: cancel}
	r := mux.NewRouter()
	r.HandleFunc("/", HomeHandler)
	r.HandleFunc("/exit", serverHelper.ExitHandler)

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

	// Wait till a cancel is executed
	<-stopHTTPServerCtx.Done()
	if err := srv.Shutdown(stopHTTPServerCtx); err != nil && err != context.Canceled {
		panic(err) // failure/timeout shutting down the server gracefully
	}
	fmt.Println("Server closed - Context")
}
```

From the above example, let's create a `httpServerHelper` structure with `cancelFunc` of type `context.CancelFunc` (line 13-15). The `context.WithCancel()`, returns a context and a cancel function, lets assign it to `stopHTTPServerCtx` and `cancel` (line 36), assign the `cancel()` function to `httpServerHelper` structure's `cancelFunc` and call it `serverHelper` (line 37). When you go to `http://127.0.0.1:8000/exit`, `cancel()` function is invoked which sends a `Done()` signal at line `61`. where there is no error and all the channels are executed, `context.Canceled` returns a string else an Error.

## Using with WaitGroup

Unlike channels and context, SyncGroup doesn't use channels but uses a low level "mutual exclusion locks". `sync.WaitGroup` structure has three functions `Add()`, `Done()`, and `Wait()`. `Add()` takes in an integer value greater than `1`, `Done()` decrements the integer value by `1`, and `Wait()` stops the program going further till the integer becomes `0`.

See [play.golang.org/p/OkdAXI8DdOz](https://play.golang.org/p/OkdAXI8DdOz)

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	wg := &sync.WaitGroup{}
	wg.Add(1) // initialValue=1

	go func() {
		fmt.Println("Hello from gorutine")
		// Hello from gorutine
		time.Sleep(2 * time.Second) // wait for two seconds
		wg.Done() // finalValue=(initialValue-1)
	}()

	wg.Wait() // if finalValue<0 break; else wait
	fmt.Println("Hello World!")
	// Hello World!
}
```

In the above example assign `sync.WaitGroup{}` to `wg`, because there is only one gorutine so adding `1` should be enough, if there are say four gorutine then you should have `wg.Add(4)` also, `wg.Done()` should be called four times. Once, gorutine reaches `wg.Done()` the `1` is decremented to `0`, `eg.Wait()` check for it and continues the program.

```go {linenos=table,hl_lines=[14,26,37,62]}
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/gorilla/mux"
)

var wg sync.WaitGroup

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, err := fmt.Fprintln(w, "<h1>Home of SyncGroup</h1><br><a href='/exit'>Exit</a>")
	if err != nil {
		panic(err)
	}
}

func ExitHandler(w http.ResponseWriter, r *http.Request) {
	// subtract 1 from the WaitGroup
	defer wg.Done()
	w.WriteHeader(http.StatusOK)
	_, err := fmt.Fprintln(w, "<h1>Bye from SyncGroup</h1>")
	if err != nil {
		panic(err)
	}
}

func main() {

	// add an integer, as there is only one exit that we want so add 1
	wg.Add(1)

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

	// wait till the counter becomes 0
	wg.Wait()

	if err := srv.Shutdown(context.TODO()); err != nil {
		panic(err) // failure/timeout shutting down the server gracefully
	}
	fmt.Println("Server closed - SyncGroup")
}
```

In the above program, let's create a global variable `wg` of type `sync.WaitGroup` (line 14). In the `main()` function add `wg.Add(1)` (line 37). In the `ExitHandler` add `defer wg.Done()` (line 26), the `defer` keyword executes at the end of function. `wg.Wait()` check id the counter has turned to zero or not, in this it would when you visit `http://127.0.0.1:8000/exit`, this then continues to the next line.

## Conclusion

Channels are the primary feature of Go language's coroutines, but they make it easier for users to use different ways to control the execution of coroutines in a program. It is up to you which one to use and it mostly depends on the program too, for a simple coroutines communication, channels should absolutely fine. Context on the other hand was made to use with servers but can also be used in simple programs. The sync library was developed to have low-level APIs for Go language to use internally but SyncGroup can be used as a high-level API to control coroutines execution.

I hope this post helps you in choosing the right one.
