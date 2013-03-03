;$verb($player, "say", $god, "rx")
;set_verb_args($player, "say", {"any", "none", "none"});
program $player:say
	this:cmd_say(
		[
			"command" -> "say",
			"text" -> argstr
		]
	);
.
