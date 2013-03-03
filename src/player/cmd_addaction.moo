;$verb($player, "cmd_addaction", $god, "rx")
program $player:cmd_addaction
	set_task_perms(caller_perms());
	{message} = args;
	
	template = $cast(message["room"], $room);
	template:checktemplate();

	template:add_action(message["description"], message["target"]);
	player:cmd_actions();
.
