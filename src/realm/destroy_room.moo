;$verb($realm, "destroy_room", $god)
program $realm:destroy_room
	set_task_perms(caller_perms());
	this:checkrealm();
	{template} = args;
	
	if (!(template in this.contents))
		raise(E_PERM, "room template not in specified realm");
	endif
	
	recycle(template);
.
