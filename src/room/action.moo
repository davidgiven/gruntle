;$verb($room, "action", $god)
program $room:action
	set_task_perms(this.owner);
	
	{id} = args;
	if (this:istemplate())
		raise(E_INVARG, "Actions can only be performed on instantiated rooms.");
	endif

	action = this.actions[id];
	type = action["type"];
	target = action["target"];
	
	player:tell("> ", action["description"]);

	if (type == "room")
		targetroom = this:instance():find_room(target);
		player:moveTo(targetroom);
	elseif (type == "message")
		player:tell(target);
	elseif (type == "script")
		mlines = {};
		for s in (decode_binary(target))
			if (typeof(s) == STR)
				mlines = listappend(mlines, s);
			elseif ((s == 10) || (s == 13))
				/* do nothing */
			else
				raise(E_INVARG, "invalid character in script");
			endif
		endfor
		
		{r, e} = eval(@mlines);
		if (!r)
			e = generate_json(e);
			player:tell(tostr("script error:", e)); 
		endif
	endif
.
