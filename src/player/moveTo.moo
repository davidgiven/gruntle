;$verb($player, "moveTo", $god)
program $player:moveTo
	set_task_perms(this);
	{destination} = args;

	move(this, destination);
	this:cmd_look();
.
