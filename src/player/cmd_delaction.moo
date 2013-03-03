;$verb($player, "cmd_delaction", $god, "rx")
program $player:cmd_delaction
	set_task_perms(this);
	template = player.location:template();
	if (template.owner != player)
		raise(E_PERM, "You don't own this realm.");
	endif

	{message} = args;
	id = toint(message["actionid"]);
	template:del_action(id);
	player:cmd_actions();
.
