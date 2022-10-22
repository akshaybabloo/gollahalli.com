# Gollahalli.com Website

Contents for [gollahalli.com](https://www.gollahalli.com).

Based on Hugo 0.56+

## 1. Run the Website

Download load and install the latest NodeJS.

Change directory to `gollahalli.com` (if not already there) and install the dependencies

```sh
yarn install
```

Generate the JS and CSS files for production

```sh
yarn build-prod
```

Copy the files using `gulp`

```sh
yarn static
```

Run the server

```sh
hugo serve
```
