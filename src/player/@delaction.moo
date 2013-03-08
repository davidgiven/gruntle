;$verb($player, "@delaction", $god, "rx")
;set_verb_args($player, "@delaction", {"any", "none", "none"});
program $player:@delaction
	$restrict_to_server();

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

	actions = mapdelete(template.actions, id);
	template:edit_room($nothing, $nothing, $nothing, actions);
	player:tell("Action ", id, " removed.");
.
