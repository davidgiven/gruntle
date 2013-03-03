;$verb($player, "@players", $god, "rx")
;set_verb_args($player, "@players", {"any", "none", "none"});
program $player:@players
	$restrict_to_server();

	this:tell("Players:");
	cp = connected_players();
	count = 0;
	for p in (players())
		s = {"  ", p.name, " (", p, ") "};
		if (p in cp)
			s = listappend(s, "(connected)");
		endif
		this:tell(@s);
		count = count + 1;
	endfor
	this:tell("(total: ", count, ")");
.
