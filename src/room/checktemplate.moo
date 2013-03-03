;$verb($room, "checktemplate", $god)
program $room:checktemplate
	set_task_perms(caller_perms());
	if (!this:istemplate())
		raise(E_INVARG, "not a room template");
	endif
.
