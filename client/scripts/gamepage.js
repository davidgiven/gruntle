(function()
{
	"use strict";

	var content = null;
	var pending_look = null;
	var pending_actions = null;
	var current_text_div = null;
	var current_actions_div = null;
	var current_status_div = null;
	var shown_user_list = false;
	
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
            		
            		current_text_div = $("<div class='room'/>");
            		content.append(current_text_div);
                	
            		current_actions_div = $("<div class='actions'/>");
            		content.append(current_actions_div);
                	
            		current_status_div = $("<div class='status'/>");
            		content.append(current_status_div);

                    $("#chatinput").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
                            {
                            	var msg = $("#chatinput").prop("value");
                            	$("#chatinput").prop("value", "");
                            	msg = msg.trim();
                            	if (msg != "")
                            	{
                            		W.Socket.Send(
                            			{
                            				command: "say",
                            				text: msg
                            			}
                            		);
                            	}
                            }
                        }
                    );

            		update_game_page();
            	}
            );
        },
        
        MovedEvent: function(message)
        {
        	current_actions_div.remove();
        	current_text_div.addClass("scrollback");
        	current_status_div.addClass("scrollback");
        
    		current_text_div = $("<div class='room'/>");
    		content.append(current_text_div);
        	
    		var top = $("#padding").offset().top - 50;
    		$.scrollTo(top,
    			{
    				duration: 0
    			}
    		);
        	
    		current_actions_div = $("<div class='actions'/>");
    		content.append(current_actions_div);
        	
    		current_status_div = $("<div class='status'/>");
    		content.append(current_status_div);
    		
    		shown_user_list = false;
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
        	
        	var header = $("<h1/>").text(message.title);
        	var body = $("<p/>").text(message.description);
        	
        	current_text_div.empty();
        	current_text_div.append(header, body);
        	
        	if (!shown_user_list)
        	{
        		$.each(message.contents,
        			function(name, uid)
        			{
        				if (uid != W.Userid)
        				{
            				var m = $("<p/>");
            				m.text(name+" is here.");
            				
            				current_status_div.append(m);
        				}
        			}
        		);
        		
        		shown_user_list = true;
        	}
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
        	
        	var list = $("<ul/>");
        	var count = 0;
        	$.each(message.actions,
        		function (id, action)
        		{
            		var e = $("<a href='#'/>");
            		e.text(action.description);
            		
            		e.click(
            			function()
                		{
                			W.Socket.Send(
                				{
                				 	command: "action",
                				 	actionid: id
                				}
                			);
                		}
            		);
            		
            		var li = $("<li/>");
            		li.append(e);
            		list.append(li);
            		
            		count++;
        		}
        	);
        	
        	current_actions_div.empty();
        	if (count > 0)
        	{
            	current_actions_div.append("<p>Would you like to:</p>");
            	current_actions_div.append(list);
        	}
        },
        
        ArrivedEvent: function(message)
        {
        	if (!current_status_div)
        		return;
        	
			var m = $("<p/>");
			m.text(message.user+" has arrived.");
			
			current_status_div.append(m);
        },
        
        DepartedEvent: function(message)
        {
        	if (!current_status_div)
        		return;
        	
			var m = $("<p/>");
			m.text(message.user+" has left.");
			
			current_status_div.append(m);
        },
        
        SpeechEvent: function(message)
        {
        	var s;
        	if (message.uid === W.Userid)
        		s = 'You say, "';
        	else
        		s = message.user + ' says, "';
        	s += message.text;
        	s += '".';
        	
        	var m = $("<p/>");
        	m.text(s);
        	current_status_div.append(m);
        }
    };
}
)();
