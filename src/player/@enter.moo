;$verb($player, "@enter", $god, "rx")
;set_verb_args($player, "@enter", {"any", "none", "none"});
program $player:@enter
	set_task_perms(this);
	if (!respond_to(dobj, "isinstance") || !dobj:isinstance())
		notify(player, "That's not a valid instance ID.");
	endif
	
	instance = dobj;
	room = instance:find_room("entrypoint");
	move(player, room);
	player:l();
.
