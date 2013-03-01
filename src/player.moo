# Create the player object, and change god to be a subclass of it.

;add_property(#0, "player", #-1, {$god, "r"})
;$player = create(#-1, $god)
;$player.name = "Player"
;chparent($god, $player)

# Create some useful attributes.

;add_property($player, "password", "", {$god, ""})
;add_property($player, "salt", tostr("$1$", random()), {$god, ""})

# Add some verbs for creating players.

;add_verb($player, {$god, "rxd", "create_player"}, {"this", "none", "this"})
program $player:create_player
	if (callers() && (caller_perms() != player))
		raise(E_PERM);
	endif
	if (!player.wizard)
		raise(E_PERM);
	endif

	{name, password} = args;
	newplayer = create($player, #5);
	set_player_flag(newplayer, 1);
	newplayer.owner = newplayer;
	newplayer.name = name;
	newplayer.password = crypt(password, $player.salt);
	return newplayer;
.

;add_verb($player, {$god, "rxd", "change_password"}, {"this", "none", "this"})
program $player:change_password
	if ((caller_perms() != player) && !player.wizard)
		raise(E_PERM);
	endif
	{password} = args;
	this.password = password;
.

# ...set up god.

;$god.name = "God"
;$god.password = crypt("testpassword", $player.salt)
