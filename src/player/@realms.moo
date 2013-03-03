;$verb($player, "@realms", $god, "rx")
;set_verb_args($player, "@realms", {"none", "none", "none"});
program $player:@realms
	$restrict_to_server();

	notify(player, "Realms you own:");
	
	count = 0;
	for realm in (this:realms())
		notify(player, tostr("  ", realm.name));
		for instance in (realm:instances())
			notify(player, tostr("    ", instance));
		endfor
		count = count + 1;
	endfor
	if (count == 0)
		notify(player, "(none)");
	endif
.
