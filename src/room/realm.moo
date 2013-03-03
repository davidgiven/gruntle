;$verb($room, "realm", $god)
program $room:realm
	set_task_perms(caller_perms());
	if (this.location != $nothing)
		return this.location;
	else
		return parent(this).location;
	endif
.
