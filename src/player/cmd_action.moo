;$verb($player, "cmd_action", $god)
program $player:cmd_action
	set_task_perms(caller_perms());
	{message} = args;

	id = toint(message["actionid"]);
	player.location:action(id);
.
