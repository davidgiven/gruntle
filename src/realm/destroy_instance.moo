;$verb($realm, "destroy_instance", $god)
program $realm:destroy_instance
	$permit("owner");
	this:checkrealm();
	{instance} = args;
	if (!(this in parents(instance)))
		raise(E_INVARG, "Not an instance of this realm.");
	endif
	
	for v, k in (instance.instantiated_rooms)
		recycle(v);
	endfor
	recycle(instance);
.
