;$verb($realm, "create_instance", $god)
program $realm:create_instance
	$permit("owner");
	this:checkrealm();
	instance = $nothing;
	entrypoint = $nothing;
	try
		instance = create(this, this.owner);
		instance.instantiated_rooms = {};
		return instance;
	except e (ANY)
		if (instance != $nothing)
			recycle(instance);
		endif
		if (entrypoint != $nothing)
			recycle(entrypoint);
		endif
		
		raise(@e[1..3]);
	endtry
.
