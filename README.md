# Gollahalli.com Website

Contents for [gollahalli.com](https://www.gollahalli.com).

Based on Hugo 0.56+

## 1. Run the Website

Download load and install the latest NodeJS.

Change directory to `gollahalli.com` (if not already there) and install the dependencies

```sh
npm install --workspace="themes/Spark2"
```

Generate the JS and CSS files

```sh
npm run prod --workspace="themes/Spark2"
```

Copy the files using `gulp`

```sh
npm run static --workspace="themes/Spark2"
```

Run the server

```sh
hugo serve
```

<!-- ## 2. Theme

For theme see - [https://github.com/akshaybabloo/spark-2-hugo-theme](https://github.com/akshaybabloo/spark-2-hugo-theme). -->
