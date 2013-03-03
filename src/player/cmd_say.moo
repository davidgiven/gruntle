;$verb($player, "cmd_say", $god)
program $player:cmd_say
	set_task_perms(this);
	{message} = args;
	
	player:tell(
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
