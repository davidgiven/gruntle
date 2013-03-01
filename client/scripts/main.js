(function()
{
    "use strict";
    
    window.W = {};
    W.URL = "ws://localhost:8086";

    W.OnSocketOpened = function()
    {
    	W.LoginPage.Show();
    };
    
    W.OnSocketClosed = function()
    {
    	document.write("closed!<br/>");
    };
    
    W.OnSocketError = function(event)
    {
    	document.write("error!<br/>");
    };
    
    /* Main entry point. */
    
    W.Main = function()
    {
    	W.Socket.Connect(W.URL);
    };
}
)();
