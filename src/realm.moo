# The classes that make up the Realm system.

;$property($system, "defaultroom", $god, "r")
;$defaultroom = #7

;$class("realm", "Generic Realm", $nothing);
;$realm.f = 1
;$property($realm, "entrypoint", $god, "rc")
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
		room.name = "Featureless void";
		room.description = "Unshaped nothingness stretches as far as you can see, tempting you to start shaping it.";
		realm.entrypoint = room;
		move(room, realm);
		return realm;
	except e (ANY)
		if (room != $nothing)
			recycle(room);
		endif
		if (realm != $nothing)
			recycle(realm);
		endif
		raise(@e[1..3]);
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

;$verb($realm, "accept", $god)
program $realm:accept
	{o} = args;
	return ($room in parents(o)) && (o.owner == this.owner);
.

;$verb($realm, "rooms", $god)
program $realm:rooms
	return this.contents;
.

;$verb($realm, "instances", $god)
program $realm:instances
	return children(this);
.

;$verb($realm, "instantiate_room", $god)
program $realm:instantiate_room
	$permit("owner");
	{room} = args;
	if (room.location != this)
		raise(E_INVARG, "Room not a template, or not part of this realm.");
	endif
.

# To be called on realm.
;$verb($realm, "create_instance", $god)
program $realm:create_instance
	$permit("owner");
	instance = $nothing;
	entrypoint = $nothing;
	try
		instance = create(this, this.owner);
		instance.instantiated_rooms = [];
		entrypoint = instance:find_instantiated_room(this.entrypoint);
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
	{instance} = args;
	if (!(this in parents(instance)))
		raise(E_INVARG, "This realm is not an instance.");
	endif
	
	for v, k in (instance.instantiated_rooms)
		recycle(v);
	endfor
	recycle(instance);
.

# To be called on instance.
;$verb($realm, "find_instantiated_room", $god)
program $realm:find_instantiated_room
	{room} = args;
	realm = parent(this);
	if (realm == $realm)
		raise(E_INVARG, "must call this on instance, not realm");
	endif 
	if (!(room in realm.contents))
		raise(E_INVARG, "room not part of this instance");
	endif
	
	try
		return this.instantiated_rooms[room];
	except e (ANY)
		iroom = create(room, this.owner);
		iroom.name = room.name;
		this.instantiated_rooms[room] = iroom;
		return iroom;
	endtry
.

# Room descriptions.

;$property($room, "description", $god)
;$verb($room, "description", $god)
program $room:description
	return this.description;
.
