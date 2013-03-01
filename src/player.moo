# Create the user object, and change god to be a subclass of it.

;add_property(#0, "user", #-1, {$god, "r"})
;$user = create(#-1, $god)
;$user.name = "User"
;chparent($god, $user)

# Create some useful attributes.

;add_property($user, "password", "", {$god, ""})
;add_property($user, "salt", tostr("$1$", random()), {$god, ""})

# Add some verbs for creating players.

;$verb($user, "create_player", $god)
program $user:create_player
	$permit("wizard");

	{name, password} = args;
	newplayer = create($user, #5);
	set_player_flag(newplayer, 1);
	newplayer.owner = newplayer;
	newplayer.name = name;
	newplayer.password = crypt(password, $user.salt);
	return newplayer;
.

;$verb($user, "change_password", $god)
program $user:change_password
	$permit("owner");
	
	{password} = args;
	this.password = password;
.

# ...set up god.

;$god.name = "God"
;$god.password = crypt("testpassword", $user.salt)
