(function()
{
    "use strict";
    
    var cbt =
    {
    	"loggedin": function(message)
    	{
    		W.Username = message.user;
    		W.Userid = message.uid;
    		W.GamePage.Show();
    	},
    	
    	"look": function(message)
    	{
    		W.GamePage.LookEvent(message);
    	},
    	
    	"actions": function(message)
    	{
    		W.GamePage.ActionsEvent(message);
    	},
    	
    	"arrived": function(message)
    	{
    		W.GamePage.ArrivedEvent(message);
    	},
    	
    	"departed": function(message)
    	{
    		W.GamePage.DepartedEvent(message);
    	},
    	
    	"moved": function(message)
    	{
    		W.GamePage.MovedEvent(message);
    	},
    	
    	"speech": function(message)
    	{
    		W.GamePage.SpeechEvent(message);
    	},
    	
    	"realms": function(message)
    	{
    		W.GamePage.RealmsEvent(message);
    	}
    };
    
    W.OnMessageReceived = function(s)
    {
    	var messagetype = s.event;
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
