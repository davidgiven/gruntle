;$verb($player, "@delaction", $god, "rx")
;set_verb_args($player, "@delaction", {"any", "none", "none"});
program $player:@delaction
	set_task_perms(this);
	template = player.location:template();
	if (template.owner != player)
		player:tell("You don't own this realm.");
		return;
	endif

	{id} = args;
	if (!match(id, "^[0-9]*$"))
		player:tell("You must supply a valid action ID.");
		return;
	endif 
	id = toint(id);
	
	template:del_action(id);
	player:tell("Action ", id, " removed.");
.
