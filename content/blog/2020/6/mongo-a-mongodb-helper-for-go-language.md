---
title: "Mongo: A MongoDB Helper for Go Language"
date: 2020-06-01T19:50:00+12:00
draft: false
categories: ["Software"]
tags: ["Go", "MongoDB"]
description: "Writing MongoDB APIs in Go language made easy with a twist."
images: ["/img/blog/mongo-a-mongodb-helper-for-go-language/mongo.jpg"]
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
  - imageLoc: "/img/blog/mongo-a-mongodb-helper-for-go-language/mongo.jpg"
    imageCaption: "Mongo: A MongoDB Helper for Go Language"
---

I am an avid user of MongoDB; I have used it everywhere from saving machine learning parameters to storing financial details. I have recently moved to Go language from Python/C++ and at the time of writing this article, MongoDB had its package for Go language - [mongo-go-driver](https://github.com/mongodb/mongo-go-driver).

Traditionally, whenever we create a document in a collection, the database creates a unique ID - `_id` (more on that [here](https://docs.mongodb.com/manual/core/document/#the-id-field)), this field is of type [ObjectID](https://docs.mongodb.com/manual/reference/bson-types/#objectid). ObjectID is a hexadecimal string that contains - 4-byte of timestamp value, 5-byte of a random value, 3-byte of incrementing counter.

Previously, I have used PostgreSQL, yes you can't compare RDBMS to NoSQL, but I wanted to get a flavour of it, so I created a package called [mongo](https://github.com/akshaybabloo/mongo). RDBMS type of database depends on the `id` field and are unique. Instead of using, `_id` to do your job, I have introduced `id`. This `id` filed can be used to add your UUID string.

> Having to find documents by `id` adds extra overhead, you will need to index `id` field to make things faster.

I have also tried to make the API a bit easier to use, instead of using seven lines of code, you can use two lines to do the same work.

<!--adsense-->

## How to use it?

You can install the package using Go modules

```cmd
go get github.com/akshaybabloo/mongo
```

### Adding a document

```go
import (
	"fmt"

	"github.com/akshaybabloo/mongo"
)

func main() {

	type data struct {
		Id   int    `bson:"id"`
		Name string `bson:"name"`
	}

	client := mongo.NewMongoDbClient{
		ConnectionUrl: "mongodb://localhost:27017/?retryWrites=true&w=majority",
		DatabaseName:  "test",
	}

	testData := data{
		Id:   1,
		Name: "Akshay",
	}

	done, err := client.Add("test_collection", testData)
	if err != nil {
		panic(err)
	}
	fmt.Println("The ID is:", done.InsertedID)
}
```

<!--adsense-->

### Delete a document

```go
import (
	"fmt"

	"github.com/akshaybabloo/mongo"
)

func main() {
	client := mongo.NewMongoDbClient{
		ConnectionUrl: "mongodb://localhost:27017/?retryWrites=true&w=majority",
		DatabaseName:  "test",
	}

	deleted, err := client.Delete("test_collection", 1)
	if err != nil {
		panic(err)
	}
	fmt.Println("Deleted items:", deleted.DeletedCount)
}
```

### Update a document

```go
import (
	"fmt"

	"github.com/akshaybabloo/mongo"
)

func main() {
	type data struct {
		Name string `bson:"name"`
	}

	client := mongo.NewMongoDbClient{
		ConnectionUrl: "mongodb://localhost:27017/?retryWrites=true&w=majority",
		DatabaseName:  "test",
	}

	testData := data{
		Name: "Akshay",
	}

	updated, err := client.Update("test_collection", 1, testData)
	if err != nil {
		panic(err)
	}
	fmt.Println("Modified items:", updated.ModifiedCount)
}
```

<!--adsense-->

### Get a document

```go
import (
	"fmt"

	"github.com/akshaybabloo/mongo"
)

func main() {

	type data struct {
		Id   int    `bson:"id"`
		Name string `bson:"name"`
	}

	client := mongo.NewMongoDbClient{
		ConnectionUrl: "mongodb://localhost:27017/?retryWrites=true&w=majority",
		DatabaseName:  "test",
	}

	var decodeData data
	output := client.Get("test_collection", 2).Decode(&decodeData)
	if output != nil {
		panic("No data found.")
	}
	fmt.Println(decodeData)
}
```

### Collection and DB API

In addition to the mentioned APIs, I have exposed two more APIs - `client.Collection` and `client.DB`. `client.Collection` returns `mongo.Collection`, if you are not happy with using the provided APIs you can use MongoDB driver's API directly. Like `client.Collection`, `client.DB` exposes `mongo.Database`.

## Conclusion

Most of you wouldn't even need this package, if you are into lazy coding and are coming from RDBMS, this might help you. I have tried my best to keep the tests accurate, they are not mocked, I use MongoDB community to test them.
