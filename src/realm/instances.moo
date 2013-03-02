;$verb($realm, "instances", $god)
program $realm:instances
	this:checkrealm();
	return children(this);
.
