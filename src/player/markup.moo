;$verb($player, "markup", $god)
program $player:markup
	return
		[
			"type" -> "player",
			"name" -> this.name,
			"oid" -> this
		];
.
