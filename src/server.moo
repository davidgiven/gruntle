# This is the JSON server itself.

;add_property(#0, "jsonserver", #-1, {$god, "r"})
;$jsonserver = create(#-1, $god)
;$jsonserver.name = "JSON Server"

;add_property($jsonserver, "connection", $nothing, {$god, ""})

;add_verb($jsonserver, {$god, "rxd", "do_login_command"}, {"this", "none", "this"})
program $jsonserver:do_login_command
	$restrict_to_server();
	subject = $nothing;
	if (!args)
		return;
	endif
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
	endif
	
	if (!valid(subject) || !is_player(subject))
		suspend(2);
		notify(player, "{'authfailed'}");
		subject = $nothing;
	endif

	return subject;
.

# Start server on system start.

program $kernel:server_started
	$jsonserver.connection = listen($jsonserver, 7778, 0);
.

