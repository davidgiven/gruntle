;$verb($realm, "checkinstance", $god)
program $realm:checkinstance
	if (!this:isinstance())
		raise(E_INVARG, "not an instance");
	endif
.
