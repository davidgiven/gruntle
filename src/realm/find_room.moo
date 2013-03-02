;$verb($realm, "find_room", $god)
program $realm:find_room
	{roomname} = args;
	this:checkinstance();
	realm = parent(this);

	try
		room = this.instantiated_rooms[roomname];
	except e (ANY)
		template = realm:find_room_template(roomname);
		room = create(template, this.owner);
		this.instantiated_rooms[roomname] = room;
	endtry
	return room;
.
