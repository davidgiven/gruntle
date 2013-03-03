;$verb($player, "cmd_editaction", $god, "rx")
program $player:cmd_editaction
	set_task_perms(this);
	template = player.location:template();
	if (template.owner != player)
		raise(E_PERM, "You don't own this realm.");
	endif

	{message} = args;
	id = toint(message["actionid"]);
	template:edit_action(id, message["newdescription"], message["newtarget"]);
	player:cmd_actions();
.
