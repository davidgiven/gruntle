;$verb($player, "cmd_delroom", $god)
program $player:cmd_delroom
	set_task_perms(caller_perms());
	{message} = args;
	
	room = $cast(message["room"], $room);
	room:checktemplate();
	realm = room:realm();	
	realm:destroy_room(room);
	this:cmd_realms();
.
