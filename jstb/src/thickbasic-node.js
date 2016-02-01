const fs = require("fs");
const vm = require("vm");

function include(path) {
    var code = fs.readFileSync(__dirname + "/../" + path, 'utf-8');
	vm.runInThisContext(code, path);
} 

include("gen/parser.js");
include("src/thickbasic.js");

module.exports = TB;

