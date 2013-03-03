;$verb($player, "cmd_createroom", $god)
program $player:cmd_createroom
	set_task_perms(caller_perms());

	{message} = args;
	instance = $cast(message["instance"], $realm);
	instance:checkinstance();
	realm = parent(instance);
	
	name = message["name"];
	template = realm:create_room(name);
	room = instance:find_room(template);
	move(player, room);
	this:cmd_look();
	this:cmd_realms();
.
