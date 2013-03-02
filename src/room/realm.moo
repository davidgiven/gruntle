;$verb($room, "realm", $god)
program $room:realm
	set_task_perms(caller_perms());
	return parent(this).location;
.
