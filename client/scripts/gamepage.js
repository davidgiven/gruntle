(function()
{
	"use strict";

	var roomscrolloffset = 0.0;
	var actionscrolloffset = 0.3;
	
	var content;
	var pending_look;
	var waiting_for_room_description;
	var shown_user_list;
	var realms;
	
	var current_text_div = null;
	var current_status_div = null;
	var edit_button = null;
	var editcontrols = null;
	
	var scroll_position = -1;

	var init = function()
	{
    	content = null;
    	pending_look = null;
    	realms = null;
    	waiting_for_room_description = true;
    	shown_user_list = false;
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
	    	
	    	var voffset = scroll_position - menubarheight*3;
	    	if (!room)
	    		voffset -= screenheight * 0.2;
	    	
	    	$('html, body').animate(
	    		{
	    			scrollTop: voffset,
	    			duration: W.Effects.DefaultDuration,
	    			easing: W.Effects.DefaultEasing
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
		if (W.CurrentRealm.uid == W.Userid)
		{
			var realm = null;
			if (realms)
				realm = realms.realms[W.CurrentRealm.id];
			if (realm)
				W.RealmEditor.Show(realm);
			else
			{
				/* Haven't had an update for this realm yet --- one will be
				 * along in a minute. */
			}
		}
    	else
    		W.RealmEditor.Hide();
	};

	var show_simple_markup = function(markup)
	{
    	if (!current_status_div)
    		return;
    	
		var m = $("<p/>").append(W.Markup.ToDOM(markup));
		
		current_status_div.append(m);
		W.Effects.NewText(m);
    	adjustScrolling(false);
	};
	
    W.GamePage =
    {
        Show: function ()
        {
        	init();

            $("#page").load("game.html",
            	function ()
            	{
            		console.log("game page loaded");
            		
            		W.StandardMarkup();                
            		content = $("#playarea");
            		
                    $("#chatinput").keydown(
                        function (event)
                        {
                            if (event.keyCode === 13)
                            {
                            	var msg = $("#chatinput").text();
                            	$("#chatinput").html("<br/>");
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

                    $("#warptoentrypoint")
                    	.unbind()
                    	.click(
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
                    
                    $("#actionsarea").hide();
                    $("#editbutton").hide();
                    
                    $("#menuchangepassword")
                    	.unbind()
                    	.click(W.GamePage.ChangePasswordEvent);

                    $("#menulogout")
                    	.unbind()
                    	.click(W.GamePage.LogoutEvent);
                    
            		$("#page").hide();
            		W.Effects.ShowPage($("#page"))
            			.promise()
            			.done(update_game_page);
            	}
            );
        },
        
        MovedEvent: function(message)
        {
        	current_text_div.addClass("scrollback");
        	current_status_div.addClass("scrollback");
        	if (edit_button)
        	{
       			W.Effects.RemoveButton(edit_button);
        		edit_button = null;
        	}
        	
        	waiting_for_room_description = true;
		shown_user_list = false;
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
            	jsprettify.prettifyHtml(body[0]);
            	
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
        			
        			W.Effects.ShowButton(edit_button);
            	}

            	current_text_div.append(header, body);
            	
            	if (!shown_user_list)
            	{
            		var players = [];
            		
            		$.each(message.contents,
            			function(name, uid)
            			{
            				if (uid != W.Userid)
            					players.push(
            						{
            							type: "player",
            							name: name,
            							oid: uid
            						}
            					);
            			}
            		);
            		
            		players.sort();
            		
            		if (players.length > 0)
            		{
            			var m = [];
                		
                		for (var i=0; i<(players.length-1); i++)
        				{
                			m.push(players[i]);
        					if (i < (players.length-1))
        						m.push(",");
        					m.push(" ");
        				}
                        		
        				if (players.length == 1)
        				{
        					m.push(players[i]);
                			m.push(' is here.');
        				}
                		else if (players.length > 1)
                		{
                			m.push(" and ");
                			m.push(players[players.length-1]);
                			m.push(" are here.");
                		}

        				var s = $("<p/>")
        				W.Markup.ToDOM(m).appendTo(s);
        				s.appendTo(current_status_div);
            		}
            		
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
        		W.Effects.NewText(current_text_div, current_status_div);
        	}
        	else
        	{
        		W.Effects.HideText(current_text_div).promise().done(
        			function()
        			{
                		update_text();
                		W.Effects.ShowText(current_text_div);
        			}
        		);
        	}
        	
        	var update_actions = function()
        	{
            	if (message.editable)
            	{
        			$("#actionseditbutton")
        				.show()
        				.unbind()
        				.click(
        					function()
        					{
        						W.RoomEditor.Show(message);
        						return false;
        					}
        				);
            	}
            	else
            		$("#actionseditbutton").hide();

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
            	jsprettify.prettifyHtml(list[0]);
        	};

        	var show_actions = function()
        	{
    			update_actions();
    			W.Effects.ShowActions($("#actionsarea"));
        	};
        	
        	if ($("#actionsarea").is(":visible"))
        	{
        		W.Effects.HideActions($("#actionsarea"))
        			.promise()
        			.done(show_actions);
        	}
        	else
        		show_actions();
        },
        
        ArrivedEvent: function(message)
        {
        	show_simple_markup(message.markup);
        },
        
        DepartedEvent: function(message)
        {
        	show_simple_markup(message.markup);
        },
        
        SpeechEvent: function(message)
        {
        	var s;
        	if (message.uid == W.Userid)
        		s = 'You say, "';
        	else
        		s = message.user + ' says, “';
        	s += message.text;
        	s += '"';
        	
        	var m = $("<p/>");
        	m.text(s);
    		m.css('color', W.Markup.PlayerColour(message.user));
        	m.hide();
        	jsprettify.prettifyHtml(m[0]);
        	current_status_div.append(m);
        	W.Effects.NewText(m);
        	adjustScrolling(false);
        },
        
        ActivityEvent: function(message)
        {
        	var m = $("<div/>");
        	m.textWithBreaks(message.message);
        	m.hide();
        	jsprettify.prettifyHtml(m[0]);
        	current_status_div.append(m);
        	W.Effects.NewText(m);
        	adjustScrolling(false);
        },
        
        ErrorEvent: function(message)
        {
        	var m = $("<p class='realmerror'/>")
        		.text(message.message);
        	var bq = $("<blockquote/>")
        	$.each(message.details,
        		function (_, s)
        		{
        			$("<div/>").text(s).appendTo(bq)
        		}
        	);
        	m.append(bq);
        	m.hide();
        	jsprettify.prettifyHtml(m[0]);
        	current_status_div.append(m);
        	W.Effects.NewText(m);
        	adjustScrolling(false);
        },
        	
        RealmsEvent: function(message)
        {
       		realms = message;
        	if (!content || !message)
        		return;
        	        	
        	var srl = $("#specialrealmlist");
        	srl.empty();
        	
        	$.each(message.specialrealms,
        		function (id, realm)
        		{
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
        			
        			srl.append($("<li/>").append(a));
        		}
        	);
        	
        	srl.append($("<hr/>"));
        	var li = $("<li/>");
        	$("<a href='#'>Warp to instance...</a>")
        		.click(
        			function()
        			{
        				W.GamePage.WarpToInstanceEvent();
        				return false;
        			}
        		).appendTo(li);
        	li.appendTo(srl);

        	var yrl = $("#yourrealmlist");
        	yrl.empty();
        	$.each(message.realms,
        		function (id, realm)
        		{
        			var li = $("<li/>");
        			
        			var instanceid = realm.instances[0];
        			
					var a = $("<a href='#'/>");
					a.text(realm.name)
        					
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
                			
					li.append(a);
        			yrl.append(li);
        		}
        	);

        	$("<hr/>").appendTo(yrl);
        	
        	var createbutton = $("<a href='#'>Create new realm</a>")
            	.click(
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
        	$("<li/>").append(createbutton).appendTo(yrl);
            
        	update_realm_map();
        },
        
        LogoutEvent: function()
        {
        	W.Effects.HidePage($("#page"))
        		.promise()
        		.done(W.Socket.Disconnect);
        },
        
        ChangePasswordEvent: function()
        {
        	$("#changepasswordcancelbutton")
        		.unbind()
        		.click(
        			function()
        			{
        				W.Effects.HideDialogue($("#changepassword"));
        			}
        		);

        	var changepassword_cb = function()
        	{
				var oldpassword = $("#changepasswordold").prop("value");
				var newpassword = $("#changepasswordnew").prop("value");
				var verifypassword = $("#changepasswordverify").prop("value");

				if (newpassword !== verifypassword)
				{
					W.Dialogue(
						{
							message: "The two copies of the new password " +
								"don't match.",
							positive: "OK"
						}
					);
				}
				else
				{
	        		W.Socket.Send(
	        			{
	        			 	command: "changepassword",
	        			 	oldpassword: oldpassword,
	        			 	newpassword: newpassword
	        			}
	        		);
				}
				return false;
        	};

        	$("#changepasswordokbutton")
        		.unbind()
        		.click(changepassword_cb);

			$("#changepasswordold")
				.unbind()
				.singleLineEditor(
					function()
					{
						$("#changepasswordnew").focus()
					}
				).html("<br/>");

			$("#changepasswordnew")
				.unbind()
				.singleLineEditor(
					function()
					{
						$("#changepasswordverify").focus()
					}
				).html("<br/>");

			$("#changepasswordverify")
				.unbind()
				.singleLineEditor(changepassword_cb)
				.html("<br/>");

        	return W.Effects.ShowDialogue($("#changepassword"));
        },

		ChangePasswordResultEvent: function(message)
		{
			W.Dialogue(
				{
					message: message.message,
					positive: "OK",
					positivecb:
						function()
						{
							if (message.success)
								W.Effects.HideDialogue($("#changepassword"));
						}
				}
			);
		},

        WarpToInstanceEvent: function()
        {
        	$("#warptoinstancecancelbutton")
        		.unbind()
        		.click(
        			function()
        			{
        				W.Effects.HideDialogue($("#warptoinstance"));
        			}
        		);
        	
        	var warp_cb = function()
        	{
        		W.Socket.Send(
        			{
        			 	command: "warp",
        			 	instance: $("#warptoinstanceid").text()
        			}
        		);
        		
				W.Effects.HideDialogue($("#warptoinstance"));
				return false;
        	};
        	
        	$("#warptoinstanceokbutton")
        		.unbind()
        		.click(warp_cb);

        	$("#warptoinstanceid")
        		.unbind()
        		.singleLineEditor(warp_cb)
        		.html("<br/>");
        	
        	return W.Effects.ShowDialogue($("#warptoinstance"));        	
        }
    };
}
)();
