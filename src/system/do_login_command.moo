program #0:do_login_command
	$restrict_to_server();
	if (!args)
		return;
	endif
	subject = $nothing;

	try
		if (args[1] == "connect")
			subject = $authenticate(@args[2..$]);
		elseif (args[1] == "create")
			subject = $player:create_player(@args[2..$]);
		elseif (args[1] == "guest")
			subject = $guest:create_guest();
		else
			notify(player, "*** invalid command");
		endif
	except e (ANY)
		this:_log_error(e);
	endtry
	
	if (!valid(subject) || !is_player(subject))
    	suspend(2);
    	notify(player, "*** failed");
    	subject = $nothing;
    endif

	return subject;
.
