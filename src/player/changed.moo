;$verb($player, "changed", $god)
program $player:changed
	if (this.connectionmode == "json")
		this:cmd_look();
	else
		this:tell("(Something in this room has changed.)");
	endif
.
