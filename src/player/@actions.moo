;$verb($player, "@actions", $god, "rx")
;set_verb_args($player, "@actions", {"any", "none", "none"});
program $player:@actions
	$restrict_to_server();

	template = player.location:template();
	if (template.owner != player)
		notify(player, "You don't own this realm.");
		return;
	endif

	player:tell("Actions defined on this room:");
	count = 0;
	for action, id in (template:actions())
		player:tell("  ", id, ": ", action["description"], " => ", action["target"]);
		count = count + 1;
	endfor 
	if (count == 0)
		player:tell("(none)");
	endif
.
