;$verb($realm, "create_room", $god)
program $realm:create_room
	set_task_perms(caller_perms());
	this:checkrealm();
	{name} = args;
	
	template = create($room, this.owner);
	template.name = name;
	template.title = "Featureless void";
	template.description = "Unshaped nothingness stretches as far as you can see, tempting you to start shaping it.";
	move(template, this);
	return template;
.
