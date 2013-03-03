;$verb($player, "cmd_look", $god)
program $player:cmd_look
	set_task_perms(this);

	contents = [];
	for p in (this.location.contents)
		if (is_player(p))
			contents[p.name] = p;
		endif
	endfor
	
	editable = (this.location.owner == this);
	
	player:tell(
		[
			"event" -> "look",
			"title" -> this.location:title(),
			"description" -> this.location:description(),
			"contents" -> contents,
			"editable" -> editable
		]
	);
	player:tell(
		[
			"event" -> "actions",
			"actions" -> this.location:actions(),
			"editable" -> editable
		]
	);
.
