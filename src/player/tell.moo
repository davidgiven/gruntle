;$verb($player, "tell", $god)
program $player:tell
	set_task_perms(this);
	{message, @rest} = args;

	if (typeof(message) != MAP)
		message =
			[
				"event" -> "activity",
				"message" -> tostr(@args)
			];
	endif
	
	if (this.connectionmode == "json")
		notify(this, generate_json(message));
	else
		notify(this, generate_json(message));
	endif
.
