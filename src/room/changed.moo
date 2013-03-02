;$verb($room, "changed", $god)
program $room:changed
	if (this:istemplate())
		/* Flag all instantiations of this room as being changed. */
		for child in (children(this))
			child:changed();
		endfor
	else
		/* Tell all players here that the room has changed. */
		for player in (this.contents)
			if (is_player(player))
				player:changed();
			endif
		endfor
	endif
.
