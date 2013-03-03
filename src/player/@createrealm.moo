;$verb($player, "@createrealm", $god, "rx")
;set_verb_args($player, "@createrealm", {"any", "none", "none"});
program $player:@createrealm
	set_task_perms(this);

	realm = this:create_realm(argstr);
	instance = realm:create_instance();
	notify(player, tostr("Your new realm is created and an instance has been started on ", instance, "."));
	room = instance:find_room("entrypoint");
	move(player, room);
	player:cmd_look();
	player:cmd_realms();
.
