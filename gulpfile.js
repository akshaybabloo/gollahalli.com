const {src, dest, parallel} = require('gulp');
const path = require('path');

// Following are the default paths that the files will be moved to
const cssFolderPath = './themes/Spark/assets/css/';
const jsFolderPath = './themes/Spark/assets/js/';

// Following are the files that will be moved to their locations
const cssFilesToMove = ['./node_modules/uikit/dist/css/uikit.css'];
const jsFilesToMove = ['./node_modules/uikit/dist/js/uikit.js',
    './node_modules/uikit/dist/js/uikit-icons.js',
    './node_modules/instantsearch.js/dist/instantsearch.development.js',
    './node_modules/algoliasearch/dist/algoliasearchLite.js'];

// Moves CSS files to their appropriate location
function moveCss() {
    return src(cssFilesToMove).pipe(dest(cssFolderPath));
}

// Moves JS files to their appropriate location
function moveJs() {
    return src(jsFilesToMove).pipe(dest(jsFolderPath));
}

// Run both functions in parallel
exports.default = parallel(moveCss, moveJs);
