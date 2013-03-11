;$verb($room, "announce", $god)
program $room:announce
	if (this:istemplate())
		/* Broadcast message to all intantiations of this room. */
		for child in (children(this))
			child:tell(@args);
		endfor
	else
		/* Broadcast message to all players in this room. */
		for p in (this.contents)
			if (is_player(p))
				p:tell(@args);
			endif
		endfor
	endif
.
