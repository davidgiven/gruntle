;$verb($realm, "create_room", $god)
program $realm:create_room
	set_task_perms(caller_perms());
	this:checkrealm();
	{name} = args;
	
	template = `this:find_room_template(name) ! E_RANGE => $failed_match';
	if (template != $failed_match)
		raise(E_RANGE, "This realm already contains a room with that name.");
	endif
	
	template = create($room, this.owner);
	template.name = name;
	template.title = "Featureless void";
	template.description = "Unshaped nothingness stretches as far as you can see, tempting you to start shaping it.";
	move(template, this);
	return template;
.
