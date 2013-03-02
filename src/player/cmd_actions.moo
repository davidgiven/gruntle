;$verb($player, "cmd_actions", $god)
program $player:cmd_actions
	set_task_perms(this);

	player:tell(
		[
			"event" -> "actions",
			"actions" -> this.location:actions()
		]
	);
.
