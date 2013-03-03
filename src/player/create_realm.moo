;$verb($player, "create_realm", $god)
program $player:create_realm
	set_task_perms(caller_perms());
	{name} = args;
	
	/* Create the realm. */
	
	realm = $nothing;
	room = $nothing;
	try
		realm = create($realm, this);
		realm.name = name;
		move(realm, this);
	
		/* Create the default room. */
		
		room = create($room, this);
		room.immutable = 1;
		room.name = "entrypoint";
		room.title = "Featureless void";
		room.description = "Unshaped nothingness stretches as far as you can see, tempting you to start shaping it.";
		move(room, realm);

		/* Commit changes. */

		r = realm;
		room = $nothing;
		realm = $nothing;
		return r;
	finally
		if (room != $nothing)
			recycle(room);
		endif
		if (realm != $nothing)
			recycle(realm);
		endif
	endtry
.
