;$verb($room, "accept", $god)
program $room:accept
	{o} = args;
	return is_player(o);
.
