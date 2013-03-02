(function()
{
	"use strict";

	var content = null;
	var pending_look = null;
	var pending_actions = null;
	var current_text_div = null;
	var current_actions_div = null;
	var current_status_div = null;
	
	var update_game_page = function()
	{
		if (pending_look)
			W.GamePage.LookEvent(pending_look);
		if (pending_actions)
			W.GamePage.ActionsEvent(pending_actions);
		
	};
	
    W.GamePage =
    {
        Show: function ()
        {
            $("#page").load("game.html",
            	function ()
            	{
            		content = $("#gamecontainer");
            		update_game_page();
            	}
            );
        },
        
        LookEvent: function(message)
        {
        	if (!content)
        	{
        		pending_look = message;
        		return;
        	}
        	else
        		pending_look = null;
        	
        	if (!current_text_div)
        	{
        		current_text_div = $("<div class='room'/>");
        		content.append(current_text_div);
        	}
        	
        	if (!current_actions_div)
        	{
        		current_actions_div = $("<div class='actions'/>");
        		content.append(current_actions_div);
        	}
        	
        	if (!current_status_div)
        	{
        		current_status_div = $("<div class='status'/>");
        		content.append(current_status_div);
        	}

        	var header = $("<h1/>").text(message.title);
        	var body = $("<p/>").text(message.description);
        	
        	current_text_div.append(header, body);
        },
        
        ActionsEvent: function(message)
        {
        	if (!content)
        	{
        		pending_actions = message;
        		return;
        	}
        	else
        		pending_actions = null;
        }
    };
}
)();
