;$verb($room, "istemplate", $god)
program $room:istemplate
	set_task_perms(caller_perms());
	return (this.location != $nothing);
.
