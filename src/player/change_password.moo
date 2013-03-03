;$verb($player, "change_password", $god)
program $player:change_password
	set_task_perms(caller_perms());
	
	{password} = args;
	this.password = crypt(password, $player.salt);
.
