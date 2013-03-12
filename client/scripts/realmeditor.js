(function()
{
	"use strict";

	W.RealmEditor =
	{
		Show: function(realm)
		{
			var container = $("#realmeditor .container");
			container.empty();
			
			var titlediv = $("<div class='title'/>");
			$("<span/>")
				.text(realm.name)
				.appendTo(titlediv);
			$("<a href='#' class='iconbutton'>✍</a>")
				.click(
					function()
					{
						W.RealmEditor.ShowProperties(W.CurrentRealm.id, realm);
						return false;
					}
				).appendTo(titlediv);
			titlediv.appendTo(container);
			
			$.each(realm.rooms,
				function(id, room)
				{
					var warp_cb = function()
					{
						W.Socket.Send(
							{
								command: "warp",
								instance: W.CurrentInstance,
								roomname: room.name
							}
						);
						return false;
					};
					
					var roomdiv = $("<div class='clear'/>");
					$("<a href='#' class='iconbutton dangerous tableiconleft'>✖</a>")
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
						).appendTo(roomdiv);
					$("<a href='#'/>")
						.text(room.name)
						.click(warp_cb)
						.appendTo(roomdiv);
					
					if (W.CurrentRoom === id)
						roomdiv.addClass("currentRoom");

					roomdiv
						.click(warp_cb)
    					.appendTo(container);
				}
			);

			var footerdiv = $("<div class='clear footer'/>");
			$("<a href='#'>[add room]</a>")
				.click(
					function()
					{
        				W.Socket.Send(
        					{
        						command: "createroom",
        						instance: W.CurrentInstance,
        						name: "newroomid",
        						title: "New room"
        					}
        				);
        				return false;
					}
				).appendTo(footerdiv);
			footerdiv.appendTo(container);
			
	    	return W.Effects.ShowDialogue($("#realmeditor"));
		},
		
		Hide: function()
		{
			W.RealmEditor.HideProperties();
			return W.Effects.HideDialogue($("#realmeditor"));
		},
		
		ShowProperties: function(id, realm)
		{
			$("#realmpropertiesname")
				.unbind()
				.singleLineEditor()
				.text(realm.name);
			
        	$("#realmpropertiescancelbutton")
        		.unbind()
        		.click(
        			function()
        			{
        				W.RealmEditor.HideProperties();
        				return false;
        			}
        		);

        	$("#realmpropertiessavebutton")
        		.unbind()
        		.click(
        			function()
        			{
        				var newname = $("#realmpropertiesname").text();
        				
						W.Socket.Send(
							{
								command: "renamerealm",
								realmid: id,
								newname: newname
							}
						);

        				W.RealmEditor.HideProperties();
        				return false;
        			}
        		);

			return W.Effects.ShowDialogue($("#realmproperties"));
		},
		
		HideProperties: function()
		{
			return W.Effects.HideDialogue($("#realmproperties"));
		}
	};
}
)();
