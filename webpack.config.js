const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

console.log("WP> Starting Webpack");

module.exports = {
    mode: "production",
    entry: {
        "bundle.js": [
            path.resolve(__dirname, 'node_modules/algoliasearch/dist/algoliasearchLite.js'),
            path.resolve(__dirname, 'node_modules/instantsearch.js/dist/instantsearch.development.js'),
            path.resolve(__dirname, 'node_modules/uikit/dist/js/uikit.js'),
            path.resolve(__dirname, 'node_modules/uikit/dist/js/uikit-icons.js'),
            path.resolve(__dirname, 'themes/Spark/assets/js/custom.js')
        ],
        'bundle': [
            path.resolve(__dirname, 'node_modules/uikit/dist/css/uikit.css')
        ]
    },
    output: {
        filename: "[name]",
        path: path.resolve(__dirname, 'dist')
    },
    plugins: [
        new MiniCssExtractPlugin({
            // filename: '[name]',
        }),
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                ],
            },
        ],
    },
};


