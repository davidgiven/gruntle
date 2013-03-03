;$verb($room, "exitfunc", $god)
program $room:exitfunc
	{o} = args;
	
	if (is_player(o))
		this:tell(
			[
				"event" -> "departed",
				"user" -> o.name,
				"uid" -> o
			]
		);
	endif
.
