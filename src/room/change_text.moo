;$verb($room, "change_text", $god)
program $room:change_text
	set_task_perms(caller_perms());
	this:checktemplate();
	{newname, newtitle, newdescription} = args;

	if (newname != $nothing)
		if (this.immutable)
			raise(E_PERM, "can't change the name of this room");
		endif
		this.name = newname;
	endif
	if (newtitle != $nothing)
		this.title = newtitle;
	endif
	if (newdescription != $nothing)
		this.description = newdescription;
	endif
	this:changed();
.
