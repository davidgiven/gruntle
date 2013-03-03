;$verb($room, "enterfunc", $god)
program $room:enterfunc
	{o} = args;
	
	if (is_player(o))
		this:tell(
			[
				"event" -> "arrived",
				"user" -> o.name,
				"uid" -> o
			]
		);
	endif
	
	if (o == player)
		player:tell(
			[
				"event" -> "moved"
			]
		);
	endif
.
