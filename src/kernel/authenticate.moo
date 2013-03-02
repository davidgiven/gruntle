# Overwrite the default authentication method (which is pretty naff).

program $kernel:authenticate
	$restrict_to_caller($system, "authenticate");
	{playername, password} = args;
	cpass = crypt(password, $player.salt);
	for p in (players())
		if (p.name == playername)
			if (strcmp(p.password, cpass) == 0)
				return p;
			endif
			return $nothing;
		endif
	endfor
.
