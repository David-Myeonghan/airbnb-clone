const gulp = require("gulp");

const css = () => {
	const postCSS = require("gulp-postcss");
	const sass = require("gulp-sass");
	const minify = require("gulp-csso");
	sass.compiler = require("node-sass");
	return gulp
		.src("assets/scss/styles.scss") // when it's run go to this directory,
		.pipe(sass().on("error", sass.logError)) // and turn it into sass form.
		.pipe(postCSS([require("tailwindcss"), require("autoprefixer")])) // transform it into normal css, as chrome browser cannot understand @tailwind rule
		.pipe(minify()) // minify it. make file size small.
		.pipe(gulp.dest("static/css")); // and then send the 3 lines of results into the directory
};

exports.default = css;
