(function()
{
	"use strict";

	var currentmessage;
	
	var cancel_cb = function()
	{
		W.GamePage.FadeOut($("#roomeditor"));
	};
	
	var save_cb = function()
	{
		/* Reload room title/description text. */
		
		currentmessage.name = $("#editroomid").text();
		currentmessage.title = $("#editroomname").textWithBreaks();
		currentmessage.description = $("#editdescription").textWithBreaks();
		
		/* Reload action text. */
		
		var actions = currentmessage.allactions;
		$.each(actions,
			function (id, action)
			{
				var editor = $("#editaction-"+id);
				action.type = editor.find(".containstype SELECT").val();
				action.description = editor.find(".description").textWithBreaks();
				action.target = editor.find(".target").textWithBreaks();
			}
		);
		
		W.Socket.Send(
			{
				command: "editroom",
				room: currentmessage.room,
				name: currentmessage.name,
				title: currentmessage.title,
				description: currentmessage.description,
				actions: currentmessage.allactions
			}
		);
		
		W.GamePage.FadeOut($("#roomeditor"));
	};
	
	var add_new_action = function()
	{
		var actions = currentmessage.allactions;
		
		var newid = 1;
		$.each(actions,
			function (id, action)
			{
				id = id|0;
				if (id >= newid)
					newid = id+1;
			}
		);
		
		var action =
		{
			id: newid,
			description: "<new description here>",
			target: "<new target here>"
		};
		
		actions[newid] = action;
		var editor = create_action_editor(newid, action);
		$("#editactions").before(editor);
	};
	
	var create_action_editor = function(id, action)
	{
		var tbody = $("<tbody class='action'/>");
		
		var tr1 = $("<tr/>");
		var title = $("<th>Action "+id+":</th><span>&nbsp;</span>");
		$("<a href='#' class='dangerous iconbutton tableiconright'>✖</a>")
			.click(
				function()
				{
					delete currentmessage.allactions[id];
					$("#editaction-"+id).remove();
					return false;
				}
			)
			.appendTo(title);
		title.appendTo(tr1);

		tr1.append("<td><div class='description' contenteditable='true'/></td>");
		
		var tr2 = $("<tr/>");
		tr2.append("<th class='containstype'><select class='type'>" +
			"<option value='room'>goes to room</option>" +
			"<option value='message'>tells player</option>" +
			"<option value='script'>runs script</option></select></th>");
		tr2.append("<td><div class='target' contenteditable='true'/></td>");
		
		tbody.append(tr1).append(tr2);
		
		tbody.find(".containstype SELECT").val(action.type);
		tbody.find(".description").textWithBreaks(action.description);
		tbody.find(".target").textWithBreaks(action.target);
		
		tbody.attr("id", "editaction-"+id);

		return tbody;
	};
	
	W.RoomEditor =
	{
		Show: function(message)
		{
			/* If the room editor is currently being shown, cancel it
			 * instead. */
			
			if ($("#roomeditor").is(":visible"))
			{
				cancel_cb();
				return;
			}
			
	    	/* Deep copy object (so we can change it without altering the 
	    	 * copy attached to the room upstack). */
	    	
	    	currentmessage = $.extend(true, {}, message);
	    	
	    	$("#editroomid").text(currentmessage.name);
			$("#editroomname").text(currentmessage.title);

			$("#editdescription").empty()
	    	var paras = currentmessage.description.split("\n");
	    	for (var i = 0; i < paras.length; i++)
	    		$("#editdescription").append($("<p/>").text(paras[i]));

	    	$("#roomeditor .action").remove();
        	$.each(currentmessage.allactions,
        		function (id, action)
        		{
        			var editor = create_action_editor(id, action);
        			$("#editactions").before(editor);
        		}
        	);
        	
        	$("#createactionbutton")
        		.unbind()
        		.click(
        			function()
        			{
        				add_new_action();
        				return false;
        			}
        		);

        	$("#editcancelbutton").unbind().click(cancel_cb);
        	$("#editsavebutton").unbind().click(save_cb);

	    	W.GamePage.FadeIn($("#roomeditor"));
		},
		
		Cancel: function()
		{
			cancel_cb();
		},
	};
}
)();
