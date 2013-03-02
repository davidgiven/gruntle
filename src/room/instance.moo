;$verb($room, "instance", $god)
program $room:instance
	if (this:istemplate())
		raise(E_INVARG, "room is a template");
	endif
	return this.instance;
.
