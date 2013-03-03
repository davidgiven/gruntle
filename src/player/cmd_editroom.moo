;$verb($player, "cmd_editroom", $god)
program $player:cmd_editroom
	set_task_perms(this);

	{message} = args;
	realm = $cast(message["realmid"], $realm);
	realm:checkrealm();
	template = realm:find_room_template(message["room"]);
	
	template:change_text(message["newtitle"], message["newdescription"]);
	this:cmd_realms();
.
