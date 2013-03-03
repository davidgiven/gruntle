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
	realm = this.location:realm();
	
	player:tell(
		[
			"event" -> "look",
			"instance" -> this.location:instance(),
			"realm" ->
				[
					"id" -> realm,
					"name" -> realm.name,
					"user" -> realm.owner.name,
					"uid" -> realm.owner
				],
			"title" -> this.location:title(),
			"description" -> this.location:description(),
			"contents" -> contents,
			"editable" -> editable
		]
	);
	
	this:cmd_actions();
.
