# This is a really simple text mode login system intended for test purposes.

;#0.welcome_message = "If you don't know what to do here, you shouldn't be here."
;#0.disable_passkey_login = 1

program #0:do_login_command
	$restrict_to_server();
	if (!args)
		return;
	endif
	subject = $nothing;
	if (args[1] == "connect")
		try
			subject = $authenticate(@args[2..$]);
		except e (ANY)
			this:_log_error(e);
		endtry
	elseif (args[1] == "create")
		try
			subject = $createplayer(@args[2..$]);
		except e (ANY)
			this:_log_error(e);
		endtry
	else
		notify(player, "*** invalid command");
	endif
	
	if (!valid(subject) || !is_player(subject))
    	suspend(2);
    	notify(player, "*** failed");
    	subject = $nothing;
    endif

	return subject;
.

program $kernel:authenticate
	$restrict_to_caller($system, "authenticate");
	server_log("auth");
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
