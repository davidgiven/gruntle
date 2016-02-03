"use strict";

import babelify from "babelify";
import browserify from "browserify";
import eslint from "gulp-eslint";
import glob from "glob";
import gulp from "gulp";
import jasmine from "gulp-jasmine";
import peg from "gulp-peg";
import rename from "gulp-rename";
import sourcemaps from "gulp-sourcemaps";
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
				}
			}
		))
		.pipe(eslint.format())
		.pipe(eslint.failAfterError());
});

gulp.task("build-code", ["parser"], () => {
	let b = browserify(
		{
			entries: ["src/main.js"],
			debug: true,
			paths: ["src", "gen"]
		}
	);
	b.transform(babelify);

	return b.bundle()
		.pipe(vinylSource('main.js'))
		.pipe(vinylBuffer())
		.pipe(sourcemaps.init({ loadMaps: true }))
		.pipe(sourcemaps.write("."))
		.pipe(gulp.dest("dist"));
});

gulp.task("default", ["lint", "run-tests", "build-code"]);

