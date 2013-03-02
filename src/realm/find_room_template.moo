;$verb($realm, "find_room_template", $god)
program $realm:find_room_template
	{roomname} = args;
	realm = this;
	
	if (this:isinstance())
		realm = parent(this);
	endif
	
	for room in (realm:rooms())
		if (room.name == roomname)
			return room;
		endif
	endfor
	raise(E_RANGE, "realm does not contain room with that name");
.
