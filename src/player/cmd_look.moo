;$verb($player, "cmd_look", $god)
program $player:cmd_look
	set_task_perms(caller_perms());

	contents = [];
	for p in (this.location.contents)
		if (is_player(p))
			contents[p.name] = p;
		endif
	endfor
	
	editable = (this.location.owner == this);
	realm = this.location:realm();
	
	result =
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
			"room" -> this.location:template(),
			"name" -> this.location.name,
			"title" -> this.location:title(),
			"description" -> this.location:description(),
			"contents" -> contents,
			"actions" -> this.location:actions(),
			"editable" -> editable
		];
	
	if (editable)
		result["allactions"] = this.location:template():actions();
	endif	
	
	player:tell(result);
.
