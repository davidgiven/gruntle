(function()
{
    "use strict";
    
    var cbt =
    {
    	"loggedin": function()
    	{
    		W.GamePage.Show();
    	},
    };
    
    W.OnMessageReceived = function(s)
    {
    	var messagetype = s.result;
    	if (!messagetype)
    		return;
    	var handler = cbt[messagetype];
    	if (!handler)
    	{
    		console.log("unrecognised server message '"+messagetype+"':\n"+
    			$.toJSON(s));
    		return;
    	}
    	
    	handler(s);
    };
}
)();
