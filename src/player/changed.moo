;$verb($player, "changed", $god)
program $player:changed
	if (this.connectionmode == "json")
		this:cmd_look();
		this:cmd_actions();
	else
		this:tell("(Something in this room has changed.)");
	endif
.
