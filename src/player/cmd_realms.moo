;$verb($player, "cmd_realms", $god)
program $player:cmd_realms
	set_task_perms(this);
	
	realms = [];
	for realm in (this:realms())
		instances = {};
		for instance in (realm:instances())
			instances = listappend(instances, instance);
		endfor
		
		rooms = [];
		for room in (realm.contents)
			rooms[room.name] =
				[
					"title" -> room.title
				];
		endfor
		
		realms[realm] =
			[
				"name" -> realm.name,
				"instances" -> instances,
				"rooms" -> rooms
			];
	endfor
	
	player:tell(
		[
			"event" -> "realms",
			"specialrealms" ->
				[
					$defaultrealm ->
						[
							"name" -> $defaultrealm.name,
							"instance" -> $defaultinstance
						]
				],
			"realms" -> realms
		]
	);
.
