;$verb($player, "tell", $god)
program $player:tell
	set_task_perms(this);
	{message} = args;

	if (player.connectionmode == "json")
		notify(player, generate_json(message));
	else
		notify(player, generate_json(message));
	endif
.
