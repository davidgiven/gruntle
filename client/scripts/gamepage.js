(function()
{
	"use strict";

	var content = null;
	var pending_look = null;
	var pending_actions = null;
	var pending_realms = null;
	var current_text_div = null;
	var current_actions_div = null;
	var current_status_div = null;
	var shown_user_list = false;
	var editcontrols = null;
	
	var update_game_page = function()
	{
		if (pending_look)
			W.GamePage.LookEvent(pending_look);
		if (pending_actions)
			W.GamePage.ActionsEvent(pending_actions);
		if (pending_realms)
			W.GamePage.RealmsEvent(pending_realms);
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

                    $("#warptoentrypoint").click(
                    	function (event)
                    	{
                    		W.Socket.Send(
                    			{
                    			 	command: "warp",
                    			 	instance: W.CurrentInstance
                    			}
                    		);
                    	}
                    );
                    
                    $("#warptoinstancebtn").click(
                    	function (event)
                    	{
                    		W.Socket.Send(
                    			{
                    			 	command: "warp",
                    			 	instance: $("#warptoinstance").prop("value")
                    			}
                    		);
                    	}
                    );
                    
                    $("#createnewrealm").click(
                    	function (event)
                    	{
                    		W.Socket.Send(
                    			{
                    				command: "createrealm",
                    				name: "An Empty Realm"
                    			}
                    		);
                    	}
                    );
                    	
            		update_game_page();
            	}
            );
        },
        
        MovedEvent: function(message)
        {
    		current_text_div.children().attr("contenteditable", "false");
    		current_text_div.children().removeClass("editable");

    		/*
        	current_text_div.addClass("scrollback");
        	current_status_div.addClass("scrollback");
        
        	current_text_div = $("<div class='room'/>");
    		content.append(current_text_div);
        	
    		$.scrollTo(current_text_div,
    			{
    				duration: 0
    			}
    		);
        	
        	current_actions_div.remove();
    		current_actions_div = $("<div class='actions'/>");
    		content.append(current_actions_div);
        	
    		current_status_div = $("<div class='status'/>");
    		content.append(current_status_div);
    		*/
    		
        	current_status_div.empty();
    		shown_user_list = false;
    		
    		if (editcontrols)
    		{
    			editcontrols.remove();
    			editcontrols = null;
    		}
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
        	
        	W.CurrentInstance = message.instance;
        	W.CurrentRealm = message.realm;
        	
        	$("#realmname").text(W.CurrentRealm.name);
        	$("#realmowner").text(W.CurrentRealm.user);
        	$("#instance").text(W.CurrentInstance);
        	
        	var header = $("<h1/>").text(message.title);
        	var body = $("<p/>").text(message.description);
        	
        	current_text_div.empty();
        	current_text_div.append(header, body);
        	
        	if (message.editable)
        	{
        		header.attr("contenteditable", "true");
        		body.attr("contenteditable", "true");
        		header.addClass("editable");
        		body.addClass("editable");
        		
        		var savebutton = $('<input id="savebutton" type="button" value="Save"/>');
        		var cancelbutton = $('<input id="savebutton" type="button" value="Cancel"/>');
        		
        		savebutton.click(
        			function()
        			{
        				W.Socket.Send(
        					{
        						command: "editroom",
        						newtitle: header.text(),
        						newdescription: body.text()
        					}
        				);
        			}
        		);
        		
        		cancelbutton.click(
        			function()
        			{
        				W.Socket.Send(
        					{
        						command: "look"
        					}
        				);
        			}
        		);
        		
        		var changeevent =
        			function(event)
        			{
                       	savebutton.addClass("urgent");
        			};
        			
        		header.keypress(changeevent);
        		body.keypress(changeevent);

        		editcontrols = $("<p class='edithelp'/>");
        		editcontrols.append($("<span>Edit the title or description text above and then press </span>"),
        			savebutton,
        			$("<span> or </span>"),
        			cancelbutton,
        			$("<span>.</span>"));
        		
        		current_text_div.append(editcontrols);
        	}
        	
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
        },
        
        RealmsEvent: function(message)
        {
        	if (!content)
        	{
        		pending_realms = message;
        		return;
        	}
        	else
        		pending_realms = null;
        	
        	var srl = $("#specialrealmlist");
        	srl.empty();
        	
        	var first = true;
        	$.each(message.specialrealms,
        		function (id, realm)
        		{
        			if (!first)
        				srl.append($("<span>, </span>"));
        			else
        				first = false;
        			
        			var a = $("<a href='#'/>").text(realm.name);
        			
        			a.click(
        				function()
        				{
        					W.Socket.Send(
        						{
        						 	command: "warp",
        						 	instance: realm.instance
        						}
        					);
        				}
        			);
        			
        			srl.append(a);
        		}
        	);
        	
        	var yrl = $("#yourrealmlist");
        	yrl.empty();
        	$.each(message.realms,
        		function (id, realm)
        		{
        			var li = $("<li/>");
        			var realmname = $("<span/>");
        			realmname.text(realm.name);
        			realmname.attr("contenteditable", "true");
        			realmname.addClass("editable");
        			
        			realmname.keydown(
        				function (event)
        				{
        					if (event.which == 13)
        					{
        						W.Socket.Send(
        							{
        								command: "renamerealm",
        								newname: realmname.text()
        							}
        						);
        						event.preventDefault();
        					}
        					else
        						realmname.addClass("urgent");
        				}
        			);
        			
        			li.append(realmname);
        			
        			var il = $("<span> (</span>");
        			var first = true;
        			$.each(realm.instances,
        				function (_, instanceid)
        				{
        					if (!first)
        						il.append("<span>, </span>");
        					else
        						first = false;
        					
        					var a = $("<a href='#'/>");
        					a.text(instanceid)
        					
		        			a.click(
                				function()
                				{
                					W.Socket.Send(
                						{
                						 	command: "warp",
                						 	instance: instanceid
                						}
                					);
                				}
                			);
                			
        					il.append(a);
        				}
        			);
        			if (first)
        				il.append($("<span>no instances</span>"));
        			il.append($("<span>)</span>"));
        			
        			li.append(il);
        			yrl.append(li);
        		}
        	);
        	if (yrl.children().length == 0)
        		yrl.append("<li>You don't have any realms yet</li>");
        }
    };
}
)();
