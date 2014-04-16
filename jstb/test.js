(function()
{
	"use strict";

	var req = new XMLHttpRequest();
	req.onload = function()
		{
			var data = this.responseText;
			window.alert(data);
		};
	req.open("get", "src/parser.peg", true);
	req.send();
}
)()

