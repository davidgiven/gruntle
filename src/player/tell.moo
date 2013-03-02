;$verb($player, "tell", $god)
program $player:tell
	set_task_perms(this);
	{message, @rest} = args;

	if (this.connectionmode == "json")
		notify(this, generate_json(message));
	else
		if (typeof(message) == MAP)
			notify(this, generate_json(message));
		else
			notify(this, tostr(@args));
		endif
	endif
.
