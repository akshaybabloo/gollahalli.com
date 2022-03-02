const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = (env, argv) => {
    return {
        entry: './src/app.ts',
        plugins: [
            new MiniCssExtractPlugin({
                filename: argv.mode !== "production" ? "./static/css/[name].css" : "./static/css/[name].min.css"
            })
        ],
        output: {
            filename: argv.mode !== "production" ? "./static/js/[name].js" : "./static/js/[name].min.js",
            path: path.resolve(__dirname, '.')
        },
        module: {
            rules: [
                {
                    test: /\.css$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader
                        },
                        {
                            loader: 'css-loader',
                            options: {
                                importLoaders: 1,
                            }
                        },
                        {
                            loader: 'postcss-loader'
                        }
                    ]
                },
                {
                    test: /\.(ts|js)x?$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader'
                        }
                    ]
                }
            ]
        },
        resolve: {
            extensions: ['.tsx', '.ts', '.js'],
            alias: {
                'vue$': 'vue/dist/vue.esm-browser.js'
            },
        },
        optimization: {
            minimizer: [
                new CssMinimizerPlugin(),
                new ForkTsCheckerWebpackPlugin(),
                new TerserPlugin()
            ],
        },
    }
}