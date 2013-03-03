;$verb($player, "cmd_createrealm", $god)
program $player:cmd_createrealm
	set_task_perms(caller_perms());
	{message} = args;

	realm = this:create_realm(message["name"]);
	instance = realm:create_instance();
	room = instance:find_room("entrypoint");
	move(player, room);
	player:cmd_look();
	player:cmd_realms();
.
