# Create the user object, and change god to be a subclass of it.

;$class("player", "Generic Player", $nothing)
;chparent($god, $player)

# Create some useful attributes.

;$property($player, "password", $god, "")
;$player.password = ""
;$property($player, "salt", $god, "")
;$player.salt = tostr("$1$", random())

# Add some verbs for creating players.

;$verb($player, "create_player", $god)
program $player:create_player
	$permit("wizard");

	{name, password} = args;
	newplayer = create($player, $god);
	set_player_flag(newplayer, 1);
	newplayer.owner = newplayer;
	newplayer.name = name;
	newplayer.programmer = 1;
	newplayer.password = crypt(password, $player.salt);
	move(newplayer, $defaultroom);
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
