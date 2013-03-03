;$verb($player, "cmd_addaction", $god, "rx")
program $player:cmd_addaction
	set_task_perms(this);
	template = player.location:template();
	if (template.owner != player)
		raise(E_PERM, "You don't own this realm.");
	endif

	{message} = args;
	template:add_action(message["description"], message["target"]);
	player:cmd_actions();
.
