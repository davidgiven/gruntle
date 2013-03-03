;$verb($player, "cmd_warp", $god)
program $player:cmd_warp
	set_task_perms(this);
	{message} = args;
	
	instance = $cast(message["instance"], $room);
	instance:checkinstance();

	roomname = "entrypoint";
	if (instance.owner == this)
		try
			roomname = message["roomname"];
		except e (ANY)
		endtry
	endif
	
	room = instance:find_room(roomname);
	move(player, room);
	player:l();
.
