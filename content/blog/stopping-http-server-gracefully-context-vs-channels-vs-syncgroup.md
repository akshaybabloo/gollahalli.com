---
title: "Stopping HTTP Server Gracefully: Context vs Channels vs SyncGroup"
date: 2020-02-02T13:01:03+13:00
draft: true
categories: []
tags: []
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

```go
package login

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
	"github.com/spf13/cobra"
)

var stopHTTPServerChan chan bool

var LoginCmd = &cobra.Command{
	Use:   "login",
	Short: "A command line tool for NeuCube cloud",
	Long: `NeuCube Cloud CLI can be used to upload large data-sets and soon it can also be used 
to use TOML or YAML configuration files to deploy models.`,
	Run: func(cmd *cobra.Command, args []string) {
		startServer()
	},
}

func RedirectToLogin(w http.ResponseWriter, r *http.Request) {
	http.Redirect(w, r, "https://my.neucube.io", http.StatusSeeOther)
}

func GetToken(w http.ResponseWriter, r *http.Request)  {
	_, _ = io.WriteString(w, "Bye\n")
	stopHTTPServerChan <- true
}

func TokenError(w http.ResponseWriter, r *http.Request)  {

}

func startServer() {
	stopHTTPServerChan = make(chan bool)
	r:= mux.NewRouter()
	r.HandleFunc("/", RedirectToLogin)
	r.HandleFunc("/done", GetToken)
	r.HandleFunc("/error", TokenError)

	fmt.Println("Server started")

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

	<- stopHTTPServerChan
	if err := srv.Shutdown(context.TODO()); err != nil {
		panic(err) // failure/timeout shutting down the server gracefully
	}
	os.Exit(0)
}
```

Context

```go
package login

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
	"github.com/spf13/cobra"
)

var stopHTTPServerChan chan bool

type httpServerHelper struct {
	stopHttpServer context.CancelFunc
}

var LoginCmd = &cobra.Command{
	Use:   "login",
	Short: "A command line tool for NeuCube cloud",
	Long: `NeuCube Cloud CLI can be used to upload large data-sets and soon it can also be used
to use TOML or YAML configuration files to deploy models.`,
	Run: func(cmd *cobra.Command, args []string) {
		startServer()
	},
}

func  RedirectToLogin(w http.ResponseWriter, r *http.Request) {
	http.Redirect(w, r, "https://my.neucube.io", http.StatusSeeOther)
}

func (helper *httpServerHelper) GetToken(w http.ResponseWriter, r *http.Request)  {
	_, _ = io.WriteString(w, "Bye\n")
	helper.stopHttpServer()
}

func TokenError(w http.ResponseWriter, r *http.Request)  {

}

func startServer() {
	//stopHTTPServerChan = make(chan bool)
	stopHTTPServerCtx, cancel := context.WithCancel(context.Background())
	serverHelper := &httpServerHelper{stopHttpServer:cancel}
	r:= mux.NewRouter()
	r.HandleFunc("/", RedirectToLogin)
	r.HandleFunc("/done", serverHelper.GetToken)
	r.HandleFunc("/error", TokenError)

	fmt.Println("Server started")

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

	<- stopHTTPServerCtx.Done()
	if err := srv.Shutdown(stopHTTPServerCtx); err != nil && err != context.Canceled {
		panic(err) // failure/timeout shutting down the server gracefully
	}
	os.Exit(0)
}
```
