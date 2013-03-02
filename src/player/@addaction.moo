;$verb($player, "@addaction", $god, "rx")
;set_verb_args($player, "@addaction", {"any", "none", "none"});
program $player:@addaction
	set_task_perms(this);
	template = player.location:template();
	if (template.owner != player)
		player:tell("You don't own this realm.");
		return;
	endif

	{description, target} = args;
	id = template:add_action(description, target);
	player:tell("Action ", id, " added.");
.
