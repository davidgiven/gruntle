;$verb($realm, "changed", $god)
program $realm:changed
	this:checkrealm();

	/* Flag all rooms in this realm as being changed. */
	for room in (this.contents)
		room:changed();
	endfor
.
