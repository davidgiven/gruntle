;$verb($player, "moveTo", $god)
program $player:moveTo
	{destination} = args;

	source = this.location;
	sourceroom = $isa(source, $room) &&	source:isinstance();
	destinationroom = $isa(destination, $room) && destination:isinstance(); 
	 
	simplemovement = sourceroom && destinationroom &&
		(source:instance() == destination:instance());
		
	if (sourceroom)
		/* Player is being moved from a real location. */
		
		if (simplemovement)
			/* Player is moving within an instance. */
			markup = {
				this:markup(),
				" leaves for ",
				destination:markup(),
				"."
			};
		else
			/* Player is moving between instances. */
			markup = {
				this:markup(),
				" warps out."
			};
		endif
		
		source:tell(
			[
				"event" -> "departed",
				"user" -> this.name,
				"uid" -> this,
				"markup" -> markup
			]
		);
	endif
	
	move(this, destination);
	
	if (destinationroom)
		/* Player is being moved to a real location. */
		
		if (simplemovement)
			/* Player is moving within an instance. */
			markup = {
				this:markup(),
				" arrives from ",
				source:markup(),
				"."
			};
		else
			/* Player is moving between instances. */
			markup = {
				this:markup(),
				" warps in."
			};
		endif
		
		destination:tell(
			[
				"event" -> "arrived",
				"user" -> this.name,
				"uid" -> this,
				"markup" -> markup
			]
		);
		
		this:tell(
			[
				"event" -> "moved"
			]
		);
	endif
	
	this:cmd_look();
.
