;$verb($player, "cmd_look", $god)
program $player:cmd_look
	set_task_perms(this);

	player:tell(
		[
			"event" -> "look",
			"title" -> this.location:title(),
			"description" -> this.location:description()
		]
	);
.
