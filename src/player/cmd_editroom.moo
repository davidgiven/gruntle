;$verb($player, "cmd_editroom", $god)
program $player:cmd_editroom
	set_task_perms(caller_perms());
	{message} = args;
	
	room = $cast(message["room"], $room);
	room:checktemplate();
	
	name = `message["name"] ! ANY => $nothing';
	title = `message["title"] ! ANY => $nothing';
	description = `message["description"] ! ANY => $nothing';
	actions = `message["actions"] ! ANY => $nothing';
	
	room:edit_room(name, title, description, actions);
	this:cmd_realms();
.
