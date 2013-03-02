# The classes that make up the Realm system.

;$property($system, "defaultroom", $god, "r")
;$defaultroom = #7

;$class("realm", "Generic Realm", $nothing);
;$realm.f = 1
;$property($realm, "instantiated_rooms", $god, "rc")

;$class("room", "Generic Room", #7);
;$room.f = 1

# Realm management.

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

;$verb($player, "accept", $god)
program $player:accept
	{o} = args;
	return ($realm in parents(o)) && (o.owner == this);
.

;$verb($player, "realms", $god)
program $player:realms
	return this.contents;
.

# Realms.

;$verb($realm, "isrealm", $god)
program $realm:isrealm
	return ($realm in parents(this));
.

;$verb($realm, "checkrealm", $god)
program $realm:checkrealm
	if (!this:isrealm())
		raise(E_INVARG, "not a realm");
	endif
.

;$verb($realm, "isinstance", $god)
program $realm:isinstance
	return parent(this):isrealm();
.

;$verb($realm, "checkinstance", $god)
program $realm:checkinstance
	if (!this:isinstance())
		raise(E_INVARG, "not an instance");
	endif
.

;$verb($realm, "accept", $god)
program $realm:accept
	this:checkrealm();
	{o} = args;
	return ($room in parents(o)) && (o.owner == this.owner);
.

;$verb($realm, "rooms", $god)
program $realm:rooms
	this:checkrealm();
	return this.contents;
.

;$verb($realm, "instances", $god)
program $realm:instances
	this:checkrealm();
	return children(this);
.

# To be called on realm.
;$verb($realm, "create_instance", $god)
program $realm:create_instance
	$permit("owner");
	this:checkrealm();
	instance = $nothing;
	entrypoint = $nothing;
	try
		instance = create(this, this.owner);
		instance.instantiated_rooms = [];
		return instance;
	except e (ANY)
		if (instance != $nothing)
			recycle(instance);
		endif
		if (entrypoint != $nothing)
			recycle(entrypoint);
		endif
		
		raise(@e[1..3]);
	endtry
.

# To be called on realm.
;$verb($realm, "destroy_instance", $god)
program $realm:destroy_instance
	$permit("owner");
	this:checkrealm();
	{instance} = args;
	if (!(this in parents(instance)))
		raise(E_INVARG, "Not an instance of this realm.");
	endif
	
	for v, k in (instance.instantiated_rooms)
		recycle(v);
	endfor
	recycle(instance);
.

# To be called on instance.
;$verb($realm, "find_room", $god)
program $realm:find_room
	{roomname} = args;
	this:checkinstance();
	realm = parent(this);

	try
		return this.instantiated_rooms[roomname];
	except e (ANY)
		for room in (realm:rooms())
			if (room.name == roomname)
				iroom = create(room, this.owner);
				this.instantiated_rooms[roomname] = iroom;
				return iroom;
			endif
		endfor
		raise(E_RANGE, "realm does not contain room with that name");
	endtry
.

# Room descriptions.

;$property($room, "title", $god, "rc")
;$verb($room, "title", $god)
program $room:title
	set_task_perms(caller_perms());
	return this.title;
.

;$property($room, "description", $god, "rc")
;$verb($room, "description", $god)
program $room:description
	set_task_perms(caller_perms());
	return this.description;
.

;$verb($room, "actions", $god)
program $room:actions
	set_task_perms(caller_perms());
	
	props = properties(this);
	return [];
.

