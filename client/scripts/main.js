(function()
{
    "use strict";
    
    window.W = {};

	/* Set this either to an explicit URL... */

    //W.URL = "ws://gate.cowlark.com:8086";

    /* ...or else it'll try to autodetect the URL from the current address.
     */

    if (!W.URL)
    {
        var loc = window.location;

        W.URL =
			((loc.protocol === "https") ? "wss://" : "ws://") +
            loc.host +
            ":8086";
    }

    W.OnSocketOpened = function()
    {
    	W.LoginPage.Show();
    };
    
    W.OnSocketClosed = function()
    {
    	W.Dialogue(
    		{
    			message: "Disconnected from server.",
    			positive: "Reconnect",
    			positivecb: W.Main
    		}
    	);
    };
    
    W.OnSocketError = function(event)
    {
		W.Dialogue(
			{
				message: "A WebSocket error occurred connecting to "+
					"the server. This probably means a configuration "+
					"error somewhere."
			}
		);
    };
    
    /* Main entry point. */
    
    W.Main = function()
    {
    	W.Socket.Connect(W.URL);
    };
    
    W.Logout = function()
    {
    	W.Socket.Disconnect();
    };
    
    /* Standard markup --- dialogues etc. */
    
    W.StandardMarkup = function(root)
    {
        $("#page").find(".dialogue").draggable(
        	{
        		handle: ".dialogue-title",
        		delay: 100
        	}
        ).hide();
        $("#page").find(".dialogue-title").click(
            function()
        	{
        	    var self = this;
        	    $(self).closest(".dialogue").moveToFront();
        	}
        );
        $("#page").find(".resizable").resizable();
    };
}
)();
