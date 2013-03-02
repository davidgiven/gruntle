;$property($room, "title", $god, "rc")
;$verb($room, "title", $god)
program $room:title
	set_task_perms(caller_perms());
	return this.title;
.
