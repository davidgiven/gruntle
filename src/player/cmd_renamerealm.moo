;$verb($player, "cmd_renamerealm", $god)
program $player:cmd_renamerealm
	set_task_perms(caller_perms());
	{message} = args;
	
	realm = $cast(message["realmid"], $realm);
	realm:checkrealm();
	
	realm:rename(message["newname"]);
	this:cmd_realms();
.
