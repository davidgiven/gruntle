;$verb($realm, "find_room", $god)
program $realm:find_room
	{roomname} = args;
	this:checkinstance();
	realm = parent(this);

	room = $nothing;
	for r in (this.instantiated_rooms)
		if (valid(r) && (r.name == roomname))
			room = r;
			break;
		endif
	endfor
	
	if (room == $nothing)
		template = realm:find_room_template(roomname);
		room = create(template, this.owner);
		room.instance = this;
		room.name = template.name;
		this.instantiated_rooms = setadd(this.instantiated_rooms, room);
	endif
	return room;
.
