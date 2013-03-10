(function()
{
	"use strict";

	W.RealmEditor =
	{
		Show: function(realms)
		{
			var realm = realms.realms[W.CurrentRealm.id];

			var container = $("#realmeditor .container");
			container.empty();
			
			var titlediv = $("<div class='title'/>");
			$("<span/>")
				.text(realm.name)
				.appendTo(titlediv);
			$("<a href='#' class='iconbutton'>✍</a>")
				.appendTo(titlediv);
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
			
	    	return W.GamePage.FadeIn($("#realmeditor"));
		},
		
		Hide: function()
		{
			return W.GamePage.FadeOut($("#realmeditor"));
		},
	};
}
)();
