;$verb($player, "@createroom", $god, "rx")
;set_verb_args($player, "@createroom", {"any", "none", "none"});
program $player:@createroom
	set_task_perms(this);
	realm = player.location:realm();
	if (realm.owner != player)
		notify(player, "You don't own this realm.");
		return;
	endif
	
	try
		realm:create_room(argstr);
		room = instance:find_room(argstr);
		move(player, room);
		player:l();
	except e (E_RANGE)
		notify(player, e[1]);
	endtry
.
