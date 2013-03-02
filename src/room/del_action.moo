;$verb($room, "del_action", $god)
program $room:del_action
	set_task_perms(caller_perms());
	{id} = args;

	this.actions = mapdelete(this.actions, id);
		
	this:changed();
.
