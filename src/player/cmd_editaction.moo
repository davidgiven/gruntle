;$verb($player, "cmd_editaction", $god, "rx")
program $player:cmd_editaction
	set_task_perms(this);

	{message} = args;
	instance = $cast(message["instance"], $realm);
	instance:checkinstance();
	template = instance:find_room_template(message["room"]);
	
	id = toint(message["actionid"]);
	template:edit_action(id, message["newdescription"], message["newtarget"]);
	this:cmd_actions();
.
