;$verb($player, "change_password", $god)
program $player:change_password
	$permit("owner");
	
	{password} = args;
	this.password = password;
.
