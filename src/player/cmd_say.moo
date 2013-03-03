;$verb($player, "cmd_say", $god)
program $player:cmd_say
	set_task_perms(caller_perms());
	{message} = args;
	
	this:tell(
		[
			"event" -> "speech",
			"user" -> player.name,
			"uid" -> player,
			"text" -> message["text"]
		]
	);
	this.location:tell(
		[
			"event" -> "speech",
			"user" -> player.name,
			"uid" -> player,
			"text" -> message["text"]
		]
	);
.
