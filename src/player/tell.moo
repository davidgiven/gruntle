;$verb($player, "tell", $god)
program $player:tell
	set_task_perms(this);
	{message, @rest} = args;

	if (player.connectionmode == "json")
		notify(player, generate_json(message));
	else
		if (typeof(message) == MAP)
			notify(player, generate_json(message));
		else
			notify(player, tostr(@args));
		endif
	endif
.
