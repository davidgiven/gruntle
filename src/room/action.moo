;$verb($room, "action", $god)
program $room:action
	{id} = args;
	if (this:istemplate())
		raise(E_INVARG, "Actions can only be performed on instantiated rooms.");
	endif

	action = this.actions[id];
	target = action["target"];
	targetroom = this:instance():find_room(target);
	
	move(player, targetroom);
	player:tell(["event" -> "moved"]);
	player:cmd_look();
.
