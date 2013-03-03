;$verb($realm, "rename", $god)
program $realm:rename
	$permit("owner");
	this:checkrealm();
	{name} = args;
	
	this.name = name;
	this:changed();
.
