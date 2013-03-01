# Create the user object, and change god to be a subclass of it.

;add_property(#0, "player", #-1, {$god, "r"})
;$player = create(#-1, $god)
;$player.name = "Generic Player"
;chparent($god, $player)

# Create some useful attributes.

;add_property($player, "password", "", {$god, ""})
;add_property($player, "salt", tostr("$1$", random()), {$god, ""})

# Add some verbs for creating players.

;$verb($player, "create_player", $god)
program $player:create_player
	$permit("wizard");

	{name, password} = args;
	newplayer = create($player, #5);
	set_player_flag(newplayer, 1);
	newplayer.owner = newplayer;
	newplayer.name = name;
	newplayer.password = crypt(password, $player.salt);
	return newplayer;
.

;$verb($player, "change_password", $god)
program $player:change_password
	$permit("owner");
	
	{password} = args;
	this.password = password;
.

# ...set up god.

;$god.name = "God"
;$god.password = crypt("testpassword", $player.salt)
