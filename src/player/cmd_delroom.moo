;$verb($player, "cmd_delroom", $god)
program $player:cmd_delroom
	set_task_perms(this);

	{message} = args;
	realm = $cast(message["realmid"], $realm);
	realm:checkrealm();
	template = realm:find_room_template(message["room"]);
	
	realm:destroy_room(template);
	this:cmd_realms();
.
