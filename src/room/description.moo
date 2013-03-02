;$property($room, "description", $god, "rc")
;$verb($room, "description", $god)
program $room:description
	set_task_perms(caller_perms());
	return this.description;
.
