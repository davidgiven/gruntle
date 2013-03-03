;$verb($player, "cmd_actions", $god)
program $player:cmd_actions
	set_task_perms(caller_perms());

	editable = (this.location.owner == this);
	realm = this.location:realm();

	if (editable)
		player:tell(
			[
				"event" -> "actions",
				"actions" -> this.location:actions(),
				"editable" -> editable,
				"allactions" -> this.location:template():actions()
			]
		);
	else
		player:tell(
			[
				"event" -> "actions",
				"actions" -> this.location:actions(),
				"editable" -> editable
			]
		);
	endif	
.
