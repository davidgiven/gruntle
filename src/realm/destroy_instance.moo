;$verb($realm, "destroy_instance", $god)
program $realm:destroy_instance
	set_task_perms(caller_perms());
	this:checkrealm();
	{instance} = args;
	if (!(this in parents(instance)))
		raise(E_INVARG, "Not an instance of this realm.");
	endif
	
	for r in (instance.instantiated_rooms)
		recycle(r);
	endfor
	recycle(instance);
.
