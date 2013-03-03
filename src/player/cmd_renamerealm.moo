;$verb($player, "cmd_renamerealm", $god)
program $player:cmd_renamerealm
	set_task_perms(this);
	realm = player.location:realm();
	if (realm.owner != player)
		raise(E_PERM, "You don't own this realm.");
	endif

	{message} = args;
	realm:rename(message["newname"]);
	this:cmd_realms();
.
