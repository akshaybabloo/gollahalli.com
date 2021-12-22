# Gollahalli.com Website

Contents for [gollahalli.com](https://www.gollahalli.com).

Based on Hugo 0.56+

## 1. Run the Website

Download load and install the latest NodeJS.

Then install Yarn

```sh
npm i -g yarn
```

Change directory to `gollahalli.com` (if not already there) and install the dependencies

```sh
yarn --cwd ./theme/Spark2 install
```

Generate the JS and CSS files

```sh
yarn --cwd ./theme/Spark2 prod
```

Copy the files using `gulp`

```sh
yarn --cwd ./theme/Spark2 gulp
```

Run the server

```sh
hugo serve
```

## 2. Theme

For theme see - [https://github.com/akshaybabloo/spark-2-hugo-theme](https://github.com/akshaybabloo/spark-2-hugo-theme).

## 3. Contributions

All contributions are welcome.
