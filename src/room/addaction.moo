;$verb($room, "addaction", $god, "rx")
;set_verb_args($room, "addaction", {"this", "none", "this"});
program $room:addaction
	set_task_perms(caller_perms());
	{description, type, target} = args;
	this:checktemplate();	
	
	/* The only reason for this verb to exist is during bootstrap. */
	
	actions = this.actions;
	id = 1;
	for v, k in (actions)
		if (k >= id)
			id = k+1;
		endif
	endfor
	
	actions[id] =
		[
			"description" -> description,
			"type" -> type,
			"target" -> target
		];
	
	this:edit_room($nothing, $nothing, $nothing, actions);
.
