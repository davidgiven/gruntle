;$verb($system, "isa", $god, "rx")
program $system:isa
	set_task_perms(caller_perms());
	{o, parent} = args;
	
	if (o == parent)
		return 1;
	endif

	
	for p in (parents(o))
		if (p == parent)
			return 1;
		endif
		if ($isa(p, parent))
			return 1;
		endif
	endfor
	
	return 0;
.
