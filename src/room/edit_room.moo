;$verb($room, "edit_room", $god)
program $room:edit_room
	set_task_perms(caller_perms());
	this:checktemplate();
	{newname, newtitle, newdescription, newactions} = args;

	if (newname != $nothing)
		if (this.immutable && (this.name != newname))
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
	if (newactions != $nothing)
		this.actions = [];
		for v, k in (newactions)
			this.actions[toint(k)] =
				[
					"description" -> v["description"],
					"type" -> v["type"],
					"target" -> v["target"]
				];
		endfor
	endif
	this:changed();
.
