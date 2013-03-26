;$verb($room, "isinstance", $god)
program $room:isinstance
	set_task_perms(caller_perms());
	return (this.location == $nothing);
.
