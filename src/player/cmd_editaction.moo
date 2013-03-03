;$verb($player, "cmd_editaction", $god, "rx")
program $player:cmd_editaction
	set_task_perms(this);
	{message} = args;
	
	room = $cast(message["room"], $room);
	room:checktemplate();
	
	id = toint(message["actionid"]);
	room:edit_action(id, message["newdescription"], message["newtarget"]);
	this:cmd_actions();
.
