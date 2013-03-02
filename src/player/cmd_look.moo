;$verb($player, "cmd_look", $god)
program $player:cmd_look
	set_task_perms(this);

	contents = [];
	for p in (this.location.contents)
		if (is_player(p))
			contents[p.name] = p;
		endif
	endfor
	
	player:tell(
		[
			"event" -> "look",
			"title" -> this.location:title(),
			"description" -> this.location:description(),
			"contents" -> contents
		]
	);
.
