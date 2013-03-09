(function()
{
	"use strict";

	var defaultduration = 300;
	var defaulteasing = "easeInOutQuad";
	
	var roomscrolloffset = 0.0;
	var actionscrolloffset = 0.3;
	
	var content = null;
	var pending_look = null;
	var current_text_div = null;
	var current_status_div = null;
	var waiting_for_room_description = true;
	var shown_user_list = false;
	var edit_button = null;
	var editcontrols = null;
	var realms = null;
	
	var scroll_position = -1;
	
	var fadeIn = function()
	{
		for (var i=0; i<arguments.length; i++)
		{
			$(arguments[i]).fadeIn(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
		}
	}
	
	var fadeOut = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);
		
		return s.fadeOut(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	}

	var slideUp = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);

		return s.slideUp(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	}
	
	var slideDown = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);

		return s.slideDown(
    			{
    				duration: defaultduration,
    				easing: defaulteasing
    			}
    		);
	}
	
	var fadeInText = function()
	{
		var s = $([]);
		for (var i=0; i<arguments.length; i++)
			s = s.add(arguments[i]);
		
		return s.fadeIn(
    			{
    				duration: defaultduration * 2,
    				easing: defaulteasing
    			}
    		);
	};
	
	var fadeOutAndRemove = function(e)
	{
		e.fadeOut(
			{
				duration: defaultduration,
				easing: defaulteasing,
				complete:
					function()
					{
						e.remove();
					}
			}
		);
	};
	
	var updateScrollPosition = function()
	{
		if (scroll_position == -1)
			scroll_position = $("#padding").offset().top;
	};

	var adjustScrolling = function(room)
	{
		if (room && (scroll_position == -1))
			updateScrollPosition();
		
		if (scroll_position != -1)
		{
	    	var menubarheight = $("#menubar").height();
	    	var screenheight = $(window).height();
	    	
	    	var voffset = scroll_position - menubarheight*2;
	    	if (!room)
	    		voffset -= screenheight * 0.2;
	    	
	    	$('html, body').animate(
	    		{
	    			scrollTop: voffset,
	    			duration: defaultduration,
	    			easing: defaulteasing
	    		}
	    	);
	    	
	    	scroll_position = -1;
		}
	};
	
	var update_game_page = function()
	{
		if (pending_look)
			W.GamePage.LookEvent(pending_look);
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
								return false;
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
            						return false;
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
        				return false;
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
    	FadeOut: fadeOut,
    	FadeIn: fadeIn,
    	
        Show: function ()
        {
            $("#page").load("game.html",
            	function ()
            	{
            		content = $("#playarea");
            		
                    $("#chatinput").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
                            {
                            	var msg = $("#chatinput").text();
                            	$("#chatinput").text("");
                            	msg = msg.trim();
                            	if (msg != "")
                            	{
                            		W.Socket.Send(
                            			{
                            				command: "say",
                            				text: msg
                            			}
                            		);
                            		
                            		updateScrollPosition();
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
                    		return false;
                    	}
                    );
                    
                    $("#warptoinstance").singleLineEditor(
                    	function (event)
                    	{
                    		W.Socket.Send(
                    			{
                    			 	command: "warp",
                    			 	instance: $("#warptoinstance").text()
                    			}
                    		);
                    		$("#warptoinstance").removeClass("urgent").empty();
                    		return false;
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
                    		return false;
                    	}
                    );
                    
                    $("#actionsarea").hide();
                    $("#editbutton").hide();
                    
                    $(".dialogue").draggable(
                    	{
                    		handle: "h3.dialogue-title"
                    	}
                    ).hide();
                    $(".resizable").resizable();
                    
            		update_game_page();
            	}
            );
        },
        
        MovedEvent: function(message)
        {
        	current_text_div.addClass("scrollback");
        	current_status_div.addClass("scrollback");
        	if (edit_button)
        	{
       			fadeOutAndRemove(edit_button);
        		edit_button = null;
        	}
        	
        	waiting_for_room_description = true;
        	adjustScrolling(true);
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
        	
        	var update_text = function()
        	{
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
            	
            	if (message.editable)
            	{
        			edit_button = $("#editbutton")
        				.clone()
        				.removeClass("template")
        				.appendTo(header)
        				.show()
        				.click(
        					function()
        					{
        						W.RoomEditor.Show(message);
        						return false;
        					}
        				);
        			
        			fadeIn(edit_button);
            	}

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
            	
            	update_realm_map();
        	};
        	
        	if (waiting_for_room_description)
        	{
        		waiting_for_room_description = false;
        		
        		current_text_div = $("<div class='room'/>")
        			.hide()
        			.appendTo(content);
            	
        		current_status_div = $("<div class='status'/>")
        			.hide()
        			.appendTo(content);

        		update_text();
        		fadeInText(current_text_div, current_status_div);
        	}
        	else
        	{
        		slideUp(current_text_div).promise().done(
        			function()
        			{
                		update_text();
                		slideDown(current_text_div);
        			}
        		);
        	}
        	
        	var update_actions = function()
        	{
            	var list = $("#actionslist");
            	list.empty();
            	
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
                    			
                    			updateScrollPosition();
                    			return false;
                    		}
                		);
                		
                		var li = $("<li/>");
                		li.append(e);
                		list.append(li);
                		
                		count++;
            		}
            	);
            	
            	if (count == 0)
            		list.append("<li>(There's nothing to do here.)</li>");
        	};

        	var show_actions = function()
        	{
    			update_actions();
    			
    			$("#actionsarea").show(
    				{
            			effect: "slide",
            			easing: defaulteasing,
            			duration: defaultduration,
            			direction: "down",
    				}
    			);
        	};
        	
        	if ($("#actionsarea").is(":visible"))
        	{
        		$("#actionsarea").hide(
            		{
            			effect: "slide",
            			easing: defaulteasing,
            			duration: defaultduration,
            			direction: "down",
            			complete: show_actions
            		}
            	);
        	}
        	else
        		show_actions();
        },
        
        ArrivedEvent: function(message)
        {
        	if (!current_status_div)
        		return;
        	
			var m = $("<p/>");
			m.text(message.user+" has arrived.");
			
			current_status_div.append(m);
			fadeInText(m);
        	adjustScrolling(false);
        },
        
        DepartedEvent: function(message)
        {
        	if (!current_status_div)
        		return;
        	
			var m = $("<p/>");
			m.text(message.user+" has left.");
			
			current_status_div.append(m);
			fadeInText(m);
        	adjustScrolling(false);
        },
        
        SpeechEvent: function(message)
        {
        	var s;
        	if (message.uid === W.Userid)
        		s = 'You say, “';
        	else
        		s = message.user + ' says, “';
        	s += message.text;
        	s += '”';
        	
        	var m = $("<p/>");
        	m.text(s);
        	m.hide();
        	current_status_div.append(m);
        	fadeInText(m);
        	adjustScrolling(false);
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
                    		return false;
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
                            		return false;
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
