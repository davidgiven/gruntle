;$verb($player, "cmd_warp", $god)
program $player:cmd_warp
	set_task_perms(this);

	{message} = args;
	instance = toobj(message["instance"]);
	if (!respond_to(instance, "isinstance") || !instance:isinstance())
		raise(E_INVARG, "That's not a valid instance ID.");
	endif
	
	room = instance:find_room("entrypoint");
	move(player, room);
	player:l();
.
