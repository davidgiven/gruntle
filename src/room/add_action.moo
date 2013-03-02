;$verb($room, "add_action", $god)
program $room:add_action
	set_task_perms(caller_perms());
	{description, target} = args;
	
	id = this.actionid;
	this.actionid = this.actionid + 1;
	
	this.actions[id] =
		[
			"description" -> description,
			"target" -> target
		];
		
	this:changed();
	return id;
.
