;$verb($player, "a*ction", $god, "rx")
;set_verb_args($player, "a", {"any", "none", "none"});
program $player:a
	set_task_perms(this);

	{id} = args;
	if (!match(id, "^[0-9]*$"))
		player:tell("You must supply a valid action ID.");
		return;
	endif 
	id = toint(id);
	
	player.location:action(id);
.
