;$verb($player, "a*ction", $god, "rx")
;set_verb_args($player, "a", {"any", "none", "none"});
program $player:a
	$restrict_to_server();

	{id} = args;
	if (!match(id, "^[0-9]*$"))
		player:tell("You must supply a valid action ID.");
		return;
	endif 
	id = toint(id);
	
	player.location:action(id);
.
