;$verb($player, "cmd_delaction", $god, "rx")
program $player:cmd_delaction
	set_task_perms(this);
	{message} = args;
	
	room = $cast(message["room"], $room);
	room:checktemplate();

	id = toint(message["actionid"]);
	room:del_action(id);
	player:cmd_actions();
.
