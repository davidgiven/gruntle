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
	
	defaultroom = $defaultinstance:find_room("entrypoint");
	move(newplayer, defaultroom);
	
	return newplayer;
.
