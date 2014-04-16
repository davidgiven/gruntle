(function()
{
	"use strict";
	var parser;

	var init = function(pegtext)
	{
		parser = PEG.buildParser(pegtext,
			{
				allowedStartRules: ["expression"]
			}
		);
		var o = parser.parse("foo+1");
		document.write(o);
	};

	var getpegtext = function(tag)
	{
		if (tag.src)
		{
			var req = new XMLHttpRequest();
			req.onload = function()
				{
					var data = this.responseText;
					init(data);
				};
			req.open("get", tag.src, true);
			req.send();
		}
		else
			init(tag.innerText);
	};

	/* Find the script tag with our parser in it. */

	var es = document.getElementsByTagName("SCRIPT");
	for (var i=0; i<es.length; i++)
	{
		var e = es[i];
		if (e.type == "application/x-thickbasic-peg")
		{
			getpegtext(e);
			return;
		}
	}
	throw "thickbasic: could not find peg script";
}
)()

