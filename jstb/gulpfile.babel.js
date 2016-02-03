"use strict";

import babelify from "babelify";
import browserify from "browserify";
import gulp from "gulp";
import rename from "gulp-rename";
import vinylSource from "vinyl-source-stream";
import sourcemaps from "gulp-sourcemaps";
import vinylBuffer from "vinyl-buffer";
import peg from "gulp-peg";
import jasmine from "gulp-jasmine";
import glob from "glob";

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

gulp.task("build-tests", ["parser"], () => {
	let b = browserify(
		{
			entries: glob.sync("tests/**/*.js"),
			debug: true,
			paths: ["src", "tests", "gen"]
		}
	);
	b.transform(babelify);

	return b.bundle()
		.pipe(vinylSource('tests.js'))
		.pipe(vinylBuffer())
		.pipe(sourcemaps.init({ loadMaps: true }))
		.pipe(sourcemaps.write("."))
		.pipe(gulp.dest("gen"));
});

gulp.task("run-tests", ["build-tests"], () => {
	return gulp.src("gen/tests.js")
		.pipe(jasmine())
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

gulp.task("default", ["run-tests", "build-code"]);

