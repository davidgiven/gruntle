;$verb($guest, "create_guest", $god)
program $guest:create_guest
	set_task_perms(caller_perms());

	if (typeof(this.all_guests) != LIST)
		this.all_guests = LIST;
	endif
	
	/* Look for an already created guest that's not in use. */

	guest = $nothing;
	connected = connected_players();
	for p in (this.all_guests)
		if (!(p in connected))
			guest = p;
			break;
		endif
	endfor

	/* If we didn't find a guest, create one. */

	if (guest == $nothing)
		guest = create($guest, $god);
		set_player_flag(guest, 1);
		guest.owner = guest;
		guest.name = tostr("Guest ", guest);
		guest.programmer = 1;
		guest.password = "nopassword";
		this.all_guests = setadd(this.all_guests, guest);
	endif

	defaultroom = $defaultinstance:find_room("entrypoint");
	move(guest, defaultroom);

	return guest;
.

