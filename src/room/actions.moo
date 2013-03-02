;$verb($room, "actions", $god)
program $room:actions
	set_task_perms(caller_perms());
	
	props = properties(this);
	return [];
.
