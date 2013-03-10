(function()
{
	"use strict";

	W.Dialogue =
		function(options)
		{
			$("#alertdialoguemessage").text(options.message);
			
			var hide_then = function(cb)
			{
				W.Effects.HideDialogue($("#alertdialogue"))
					.promise()
					.done(
						function()
						{
							if (cb)
								cb();
						}
					);
			};
			
			if (options.positive)
				$("#alertpositivebutton")
					.show()
					.val(options.positive)
					.unbind()
					.click(
						function()
						{
							hide_then(options.positivecb)
							return false;
						}
					);
			else
				$("#alertpositivebutton").hide();
			
			if (options.negative)
				$("#alertnegativebutton")
					.show()
					.val(options.negative)
					.unbind()
					.click(
						function()
						{
							hide_then(options.negativecb)
							return false;
						}
					);
			else
				$("#alertnegativebutton").hide();
			
			$("#alertdialogue .dialogue").show();
			W.Effects.ShowDialogue($("#alertdialogue"));
		};
}
)();
