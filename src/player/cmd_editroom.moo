;$verb($player, "cmd_editroom", $god)
program $player:cmd_editroom
	set_task_perms(this);
	template = player.location:template();
	if (template.owner != player)
		raise(E_PERM, "You don't own this realm.");
	endif

	{message} = args;
	template:change_text(message["newtitle"], message["newdescription"]);
.
