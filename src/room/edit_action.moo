;$verb($room, "edit_action", $god)
program $room:edit_action
	set_task_perms(caller_perms());
	{id, description, target} = args;
	
	this.actions[id] =
		[
			"description" -> description,
			"target" -> target
		];
		
	this:changed();
	return id;
.
