;$verb($player, "cmd_action", $god)
program $player:cmd_action
	set_task_perms(this);
	{message} = args;

	id = toint(message["actionid"]);
	player.location:action(id);
.
