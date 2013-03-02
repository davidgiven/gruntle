;$verb($player, "create_realm", $god)
program $player:create_realm
	set_task_perms(this);
	{name} = args;
	
	/* Does the player have a realm of this name already? */
	
	for o in (this.contents)
		if ($realm in parents(o))
			if (name == o.name)
				raise(E_RANGE, "You already have a realm of that name.");
			endif
		endif
	endfor
	
	/* Create the realm. */
	
	realm = $nothing;
	room = $nothing;
	try
		realm = create($realm, this);
		realm.name = name;
		move(realm, this);
	
		/* Create the default room. */
		
		room = create($room, this);
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
