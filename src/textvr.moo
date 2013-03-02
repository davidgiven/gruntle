# Some really basic text VR verbs to give console users something to see.

;$verb($player, "l*ook", $god, "rx")
;set_verb_args($player, "l", {"none", "none", "none"});
program $player:l
	r = player:cmd_look();
.

;$verb($system, "user_connected", $god, "rx")
program $system:user_connected
	player.connectionmode = "text";
	player:l();
.

;$verb($system, "user_created", $god, "rx")
program $system:user_created
	this:user_connected();
.

;$verb($system, "user_reconnected", $god, "rx")
program $system:user_reconnected
	this:user_connected();
.

;$verb($player, "@realms", $god, "rx")
;set_verb_args($player, "@realms", {"none", "none", "none"});
program $player:@realms
	set_task_perms(this);
	notify(player, "Realms you own:");
	
	count = 0;
	for realm in (this:realms())
		notify(player, tostr("  ", realm.name));
		for instance in (realm:instances())
			notify(player, tostr("    ", instance));
		endfor
		count = count + 1;
	endfor
	if (count == 0)
		notify(player, "(none)");
	endif
.

;$verb($player, "@createrealm", $god, "rx")
;set_verb_args($player, "@createrealm", {"any", "none", "none"});
program $player:@createrealm
	set_task_perms(this);
	try
		realm = this:create_realm(argstr);
		instance = realm:create_instance();
		notify(player, tostr("Your new realm is created and an instance has been started on ", instance, "."));
		room = instance:find_room("entrypoint");
		move(player, room);
		player:l();
	except e (E_RANGE)
		notify(player, e[1]);
	endtry
.

;$verb($player, "@enter", $god, "rx")
;set_verb_args($player, "@enter", {"any", "none", "none"});
program $player:@enter
	set_task_perms(this);
	if (!respond_to(dobj, "isinstance") || !dobj:isinstance())
		notify(player, "That's not a valid instance ID.");
	endif
	
	instance = dobj;
	room = instance:find_room("entrypoint");
	move(player, room);
	player:l();
.
