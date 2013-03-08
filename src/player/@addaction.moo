;$verb($player, "@addaction", $god, "rx")
;set_verb_args($player, "@addaction", {"any", "none", "none"});
program $player:@addaction
	set_task_perms(caller_perms());

	template = player.location:template();
	if (template.owner != player)
		player:tell("You don't own this realm.");
		return;
	endif

	{description, type, target} = args;
	
	actions = template.actions;
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
	
	template:edit_room($nothing, $nothing, $nothing, actions);
	player:tell("Action ", id, " added.");
.
