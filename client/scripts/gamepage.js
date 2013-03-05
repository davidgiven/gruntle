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
	var editcontrols = null;
	var realms = null;
	
	var update_game_page = function()
	{
		if (pending_look)
			W.GamePage.LookEvent(pending_look);
		if (pending_actions)
			W.GamePage.ActionsEvent(pending_actions);
		if (realms)
			W.GamePage.RealmsEvent(realms);
	};
	
	var update_realm_map = function()
	{
		if (W.CurrentRealm.uid === W.Userid)
    		show_realm_map();
    	else
    		hide_realm_map();
	};

	var show_realm_map = function()
	{
		if (!realms)
			return;
		
		var realm = realms.realms[W.CurrentRealm.id];
		if (!realm)
		{
			/* We haven't received an update with this realm data in it ---
			 * one will be along in a moment.
			 */
			hide_realm_map();
			return;
		}
		
		var map = $("#realmmap");
		map.show();
		map.empty();
		
		map.append("<p>Rooms in this realm:</p>");
		
		var ul = $("<ul/>");
		var count = 0;
		$.each(realm.rooms,
			function (id, room)
			{
				var li = $("<li/>");
				var t = $("<span/>").text(room.title);
				var n = $("<span/>").text(room.name);
				
				var changed_cb = function()
				{
					var msg =
						{
							command: "editroom",
							room: id,
							newtitle: t.text()
						};
					
					if (!room.immutable)
						msg.newname = n.text();
					
					W.Socket.Send(msg);
				};
				
				if (!room.immutable)
					n.singleLineEditor(changed_cb);
				t.singleLineEditor(changed_cb);
				
				if (W.CurrentRoom === id)
					li.addClass("currentRoom");
				
				li.append(n, " ⇒ ", t, " ");
				li.append(
					$("<a href='#'>[Warp]</a>")
						.click(
							function()
							{
								W.Socket.Send(
									{
										command: "warp",
										instance: W.CurrentInstance,
										roomname: room.name
									}
								);
							}
						)
				);
				
				if (!room.immutable)
				{
    				li.append(" ");
    				li.append(
    					$("<a href='#'>[Delete]</a>")
    						.click(
            					function()
            					{
            						W.Socket.Send(
            							{
            								command: "delroom",
            								room: id
            							}
            						);
            					}
    						)
    				);
				}

				ul.append(li);
				count = count + 1;
			}
		);
		if (count == 0)
			ul.append("<li>(none)</li>");
		map.append(ul);
		
		map.append(
			$("<a href='#'>[Create room]</a>")
    			.click(
    				function()
    				{
        				W.Socket.Send(
        					{
        						command: "createroom",
        						instance: W.CurrentInstance,
        						name: "id",
        						title: "New room"
        					}
        				);
    				}
    			)
    	);
	};
	
	var hide_realm_map = function()
	{
		$("#realmmap").hide();
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
        	W.CurrentRoom = message.room;
        	
        	$("#realmname").text(W.CurrentRealm.name);
        	$("#realmowner").text(W.CurrentRealm.user);
        	$("#instance").text(W.CurrentInstance);
        	
        	var header = $("<h1/>").text(message.title);
        	var body = $("<div/>");

		var paras = message.description.split("\n");
		for (var i = 0; i < paras.length; i++)
			body.append($("<p/>").text(paras[i]));
        	
        	current_text_div.empty();
        	current_text_div.append(header, body);
        	
        	if (message.editable)
        	{
        		header.attr("contenteditable", "true");
        		body.attr("contenteditable", "true");
        		
        		var savebutton = $('<input id="savebutton" type="button" value="Save"/>');
        		var cancelbutton = $('<input id="savebutton" type="button" value="Cancel"/>');
        		
        		savebutton.click(
        			function()
        			{
        				W.Socket.Send(
        					{
        						command: "editroom",
        						room: message.room,
        						newtitle: header.text(),
        						newdescription: body.textWithBreaks()
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
        	
        	update_realm_map();
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
            	current_actions_div.append("<p>Things to do:</p>");
            	current_actions_div.append(list);
        	}
        	
        	if (message.editable)
        	{
        		current_actions_div.append("<p>The following actions are defined on this room:</p>");
        		
            	var list = $("<ul/>");
            	var count = 0;
            	$.each(message.allactions,
            		function (id, action)
            		{
            			var message = $("<span/>");
            			var target = $("<span/>");
            			var deletelink = $("<a href='#'>[Delete]</a>");
                		var li = $("<li/>");
                		li.append(message, $("<span> ⇒ </span>"), target,
                			"<span> </span>", deletelink);
            			
                		message.text(action.description);
                		target.text(action.target);
                		
                		var commit_cb =
                			function()
                			{
                				W.Socket.Send(
                					{
                						command: "editaction",
                						room: W.CurrentRoom,
                						actionid: id,
                						newdescription: message.text(),
                						newtarget: target.text()
                					}
                				);
                			};
                			
                		message.singleLineEditor(commit_cb);
                		target.singleLineEditor(commit_cb);
                		
                		list.append(li);
                		
                		deletelink.click(
                			function()
                			{
                				W.Socket.Send(
                					{
                						command: "delaction",
                						room: W.CurrentRoom,
                						actionid: id
                					}
                				);
                			}
                		);
                		
                		count++;
            		}
            	);
            	if (count == 0)
            		list.append($("<li><span>(you can't do anything here)</span></li>"));
            	
            	current_actions_div.append(list);
            	
            	var createlink = $("<p><a href='#'>[Create action]</a></p>")
            		.click(
            			function()
            			{
            				W.Socket.Send(
            					{
            						command: "addaction",
            						room: W.CurrentRoom,
            						description: "<description>",
            						target: "<target room>"
            					}
            				);
            			}
            		);
            	current_actions_div.append(createlink);
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
       		realms = message;
        	if (!content || !message)
        		return;
        	        	
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
        			realmname.singleLineEditor(
        				function()
        				{
    						W.Socket.Send(
    							{
    								command: "renamerealm",
    								realmid: id,
    								newname: realmname.text()
    							}
    						);
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
        	
        	update_realm_map();
        }
    };
}
)();
