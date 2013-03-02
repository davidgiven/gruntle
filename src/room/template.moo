;$verb($room, "template", $god)
program $room:template
	set_task_perms(caller_perms());
	return parent(this);
.
