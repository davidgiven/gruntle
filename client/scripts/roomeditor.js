(function()
{
	"use strict";

	var editor;
	var room;
	
	var cancel_cb = function()
	{
		W.Effects.HideDialogue($("#roomeditor"));
	};
	
	var save_cb = function()
	{
		/* Reload room title/description text. */

		var name = $("#editroomid").text();
		var title = $("#editroomname").textWithBreaks();
		var script = editor.getValue();

		W.Socket.Send(
			{
				command: "setroomdata",
				room: room,
				name: name,
				title: title,
				script: script
			}
		);

		//W.Effects.HideDialogue($("#roomeditor"));
	};

	var check_cb = function()
	{
		var script = editor.getValue();
		
		W.Socket.Send(
			{
				command: "syntaxcheck",
				script: script
			}
		);
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
			/* If the room editor is currently being shown, do nothing. */

			if ($("#roomeditor").is(":visible"))
				return;

			room = message.id;
	    	$("#editroomid").text(message.name);
			$("#editroomname").text(message.title);

			$("#codecontainer").empty();
			editor = CodeMirror($("#codecontainer")[0],
				{
					value: message.script,
                    mode: "tb",
                    lineWrapping: true,
                    lineNumbers: true,
                    tabSize: 2,
                    indentWithTabs: 2,
				}
			);

        	$("#editcancelbutton").unbind().click(cancel_cb);
        	$("#editsavebutton").unbind().click(save_cb);
        	$("#editcheckbutton").unbind().click(check_cb);

	    	W.Effects.ShowDialogue($("#roomeditor"));

	    	/* This must happen after the editor has been added to the DOM
	    	 * tree. */

	        editor.refresh();
		},
		
		Cancel: function()
		{
			cancel_cb();
		},
	};
}
)();
