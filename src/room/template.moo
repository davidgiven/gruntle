;$verb($room, "template", $god)
program $room:template
	set_task_perms(caller_perms());
	if (this:isinstance())
		return parent(this);
	else
		return this;
	endif
.
