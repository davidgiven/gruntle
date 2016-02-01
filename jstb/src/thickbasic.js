var TB = {};
(function() {
	"use strict";

	var parser = TBParser;

	TB.compile = function(text) {
		return parser.parse(text);
	};
})();

