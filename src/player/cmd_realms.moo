;$verb($player, "cmd_realms", $god)
program $player:cmd_realms
	set_task_perms(this);
	
	realms = [];
	for realm in (this:realms())
		instances = {};
		for instance in (realm:instances())
			instances = listappend(instances, instance);
		endfor
		realms[realm] =
			[
				"name" -> realm.name,
				"instances" -> instances
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
