(function()
{
	"use strict";

	W.Help =
	{
		Show: function(url)
		{
			var frame = $("#help iframe");
			frame.attr("src", url);

        	$("#helpindexbutton").unbind().click(
        	    function()
        	    {
        	        frame.attr("src", "help/index.html");
        	    }
        	);

        	$("#helpclosebutton").unbind().click(
        	    function()
        	    {
        	        W.Effects.HideDialogue($("#help"));
        	    }
        	);

	    	return W.Effects.ShowDialogue($("#help"));
		},
	};
}
)();
