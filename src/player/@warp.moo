;$verb($player, "@warp", $god, "rx")
;set_verb_args($player, "@warp", {"any", "none", "none"});
program $player:@warp
	$restrict_to_server();

	if (!respond_to(dobj, "isinstance") || !dobj:isinstance())
		notify(player, "That's not a valid instance ID.");
	endif
	
	instance = dobj;
	room = instance:find_room("entrypoint");
	move(player, room);
	player:l();
.
