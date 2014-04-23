(function()
{
	"use strict";
	var parser;

	var loadscripttext = function(tag, cb)
	{
		if (tag.src)
		{
			var req = new XMLHttpRequest();
			req.onload = function()
				{
					var data = this.responseText;
					cb(data);
				};
			req.open("get", tag.src, true);
			req.send();
		}
		else
			cb(tag.innerText);
	};

	var findscripts = function(mimetype, cb, compulsory)
	{
		var es = document.getElementsByTagName("SCRIPT");
		for (var i=0; i<es.length; i++)
		{
			var e = es[i];
			if (e.type == mimetype)
			{
				loadscripttext(e, cb);
				if (compulsory)
					return;
			}
		}
		if (compulsory)
			throw "thickbasic: could not find "+mimetype+" script";
	}

	var init = function(pegtext)
	{
		parser = PEG.buildParser(pegtext,
			{
				allowedStartRules: ["block"]
			}
		);

		findscripts("application/x-thickbasic",
			function(text)
			{
				var o = parser.parse(text);
				document.write(o);
			},
			false
		);
	};

	findscripts("application/x-thickbasic-peg", init, true);
}
)()

