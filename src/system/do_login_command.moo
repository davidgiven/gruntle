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
			subject = $player:create_player(@args[2..$]);
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
