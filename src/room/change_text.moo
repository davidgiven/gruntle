;$verb($room, "change_text", $god)
program $room:change_text
	set_task_perms(caller_perms());
	{newtitle, newdescription} = args;

	this.title = newtitle;
	this.description = newdescription;
	this:changed();
.
