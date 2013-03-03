;$verb($player, "cmd_editroom", $god)
program $player:cmd_editroom
	set_task_perms(this);
	{message} = args;
	
	room = $cast(message["room"], $room);
	room:checktemplate();
	
	name = `message["newname"] ! ANY => $nothing';
	title = `message["newtitle"] ! ANY => $nothing';
	description = `message["newdescription"] ! ANY => $nothing';
	
	room:change_text(name, title, description);
	this:cmd_realms();
.
