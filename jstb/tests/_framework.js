module.exports = {
	equals:
		function (want, got) {
			if (want !== got) {
				throw "Assertion failure: wanted " + want + ", got " + got;
			}
		}
}

