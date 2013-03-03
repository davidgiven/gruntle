;$verb($player, "@rooms", $god, "rx")
;set_verb_args($player, "@rooms", {"none", "none", "none"});
program $player:@rooms
	$restrict_to_server();

	realm = player.location:realm();
	if (realm.owner != player)
		notify(player, "You don't own this realm.");
		return;
	endif
	
	notify(player, tostr("Rooms in ", realm.name, ":"));
	count = 0;
	for room in (realm.contents)
		notify(player, tostr("  ", room.title, " (", room.name, ")"));
		count = count + 1;
	endfor
	if (count == 0)
		notify(player, "(none)");
	endif
.
