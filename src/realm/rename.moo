;$verb($realm, "rename", $god)
program $realm:rename
	set_task_perms(caller_perms());
	this:checkrealm();
	{name} = args;
	
	this.name = name;
	this:changed();
.
