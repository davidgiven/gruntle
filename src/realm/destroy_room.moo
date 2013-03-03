;$verb($realm, "destroy_room", $god)
program $realm:destroy_room
	set_task_perms(caller_perms());
	this:checkrealm();
	{template} = args;
	
	if (!(template in this.contents))
		raise(E_PERM, "room template not in specified realm");
	endif
	
	/* Make sure we don't destroy any special rooms! */
	
	if (template.immutable)
		raise(E_PERM, "this room cannot be destroyed");
	endif
	
	/* Also recycle any instances of the room, booting the contents
	 * thereof. */
	 
	destination = $defaultinstance:find_room("entrypoint");
	for c in (children(template))
		for p in (c.contents)
			move(p, destination);
		endfor
		recycle(c);
	endfor
	
	recycle(template);
.
