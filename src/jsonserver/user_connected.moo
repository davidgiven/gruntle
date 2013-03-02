;$verb($jsonserver, "user_connected", $god)
program $jsonserver:user_connected
	player.connectionmode = "json";
	player:cmd_look();
.
