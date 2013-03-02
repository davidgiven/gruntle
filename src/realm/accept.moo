;$verb($realm, "accept", $god)
program $realm:accept
	this:checkrealm();
	{o} = args;
	return ($room in parents(o)) && (o.owner == this.owner);
.
