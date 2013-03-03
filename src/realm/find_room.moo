;$verb($realm, "find_room", $god)
program $realm:find_room
	{o} = args;
	this:checkinstance();
	realm = parent(this);

	if (typeof(o) == STR)
		roomname = o;
		
		for r in (this.instantiated_rooms)
			if (valid(r) && (r.name == roomname))
				return r;
			endif
		endfor
		
		template = realm:find_room_template(roomname);
	else
		template = o;
		
		for r in (this.instantiated_rooms)
			if (valid(r) && (r:template() == template))
				return r;
			endif
		endfor
	endif
	
	/* If we got this far, we were unable to find the room in the cache, so
	 * instantiate a new one. */
	 
	room = create(template, this.owner);
	room.instance = this;
	room.name = template.name;
	this.instantiated_rooms = setadd(this.instantiated_rooms, room);
	return room;
.
