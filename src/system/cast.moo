;$verb($system, "cast", $god, "rx")
program $system:cast
	set_task_perms(caller_perms());
	{s, parent} = args;
	
	o = toobj(s);
	if (!valid(o))
		raise(E_INVIND);
	endif
	if (!$isa(o, parent))
		raise(E_INVIND);
	endif
	
	return o;
.
