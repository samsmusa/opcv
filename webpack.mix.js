const mix = require("laravel-mix");

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix
  .js("omr-rnd-api/templates/assets/js/src/index.js", "omr-rnd-api/static/js")
  .postCss(
    "omr-rnd-api/templates/assets/js/src/index.css",
    "omr-rnd-api/static/css",
    [require("tailwindcss")]
  );
