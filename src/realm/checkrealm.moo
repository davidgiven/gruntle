;$verb($realm, "checkrealm", $god)
program $realm:checkrealm
	if (!this:isrealm())
		raise(E_INVARG, "not a realm");
	endif
.
