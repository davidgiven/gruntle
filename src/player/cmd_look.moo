;$verb($player, "cmd_look", $god)
program $player:cmd_look
	set_task_perms(this);

	player:tell(
		[
			"result" -> "look",
			"roomtitle" -> this.location:title(),
			"roomdescription" -> this.location:description()
		]
	);
.
