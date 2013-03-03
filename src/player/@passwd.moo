;$verb($player, "@passwd", $god, "rx")
;set_verb_args($player, "@passwd", {"any", "none", "none"});
program $player:@passwd
	$restrict_to_server();
	{password} = args;

	this:change_password(password);
	this:tell("Password changed. (Make a note.)");
.
