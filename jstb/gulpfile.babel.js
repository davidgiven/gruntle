"use strict";

import babelify from "babelify";
import browserify from "browserify";
import eslint from "gulp-eslint";
import glob from "glob";
import gulp from "gulp";
import jasmine from "gulp-jasmine";
import less from "gulp-less";
import peg from "gulp-peg";
import rename from "gulp-rename";
import sourcemaps from "gulp-sourcemaps";
import uglify from "gulp-uglify";
import vinylBuffer from "vinyl-buffer";
import vinylSource from "vinyl-source-stream";

gulp.task("parser", () => {
	return gulp.src("src/thickbasic-parser.peg")
		.pipe(peg(
			{
				allowedStartRules: ["program"],
				cache: true
			}
		))
		.pipe(gulp.dest("gen"));
});

gulp.task("run-tests", ["parser"], () => {
	return gulp.src("tests/**/test*.js")
		.pipe(jasmine())
});

gulp.task("lint", ["parser"], () => {
	return gulp.src(["src/*.js", "tests/*.js"])
		.pipe(eslint(
			{
				parser: "babel-eslint",
				rules: {
					"strict": 0,
					"semi": 2,
					"no-unexpected-multiline": 2,
					"prefer-spread": 2,
				},
				env: {
					"browser": true,
					"commonjs": true
				}
			}
		))
		.pipe(eslint.format())
		.pipe(eslint.failAfterError());
});

gulp.task("build-code", ["parser"], () => {
	let b = browserify(
		{
			entries: [
				require.resolve("babel-polyfill"),
				"src/main.js"
			],
			debug: true,
			paths: ["src", "gen"]
		}
	);
	b.transform(babelify);

	return b.bundle()
		.pipe(vinylSource('main.js'))
		.pipe(vinylBuffer())
		.pipe(sourcemaps.init({ loadMaps: true }))
		//.pipe(uglify())
		.pipe(sourcemaps.write("."))
		.pipe(gulp.dest("dist"));
});

gulp.task("build-styles", () => {
	return gulp.src("src/styles.less")
		.pipe(less())
		.pipe(gulp.dest("dist"));
});

gulp.task("build-html", () => {
	return gulp.src("src/index.html")
		.pipe(gulp.dest("dist"));
});

gulp.task("default",
	["lint", "run-tests", "build-code", "build-styles", "build-html"]);

