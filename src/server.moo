# This is the JSON server itself.

;add_property(#0, "jsonserver", #-1, {$god, "r"})
;$jsonserver = create(#-1, $god)
;$jsonserver.name = "JSON Server"

;add_property($jsonserver, "connection", $nothing, {$god, ""})

;$verb($jsonserver, "do_login_command", $god)
program $jsonserver:do_login_command
	$restrict_to_server();
	
	set_connection_option(player, "disable-oob", 1);
	set_connection_option(player, "intrinsic-commands", 0);

	/* Check for call on initial login. */
	
	if (argstr == "")
		return;
	endif
	
	s = `parse_json(argstr) ! ANY => $nothing';
	id = `s["id"] ! ANY => 0';
	result = ["result" -> "malformed"];
	if (typeof(s) == MAP)
		command = `s["command"] ! ANY => 0';
		if (typeof(command) == STR)
			command = tostr("logincmd_", command);
			if (respond_to(this, command))
				try
					result = this:(command)(s);
					if ((typeof(result) == OBJ) && (result != $nothing))
						server_log(tostr("player ", result.name, " logged in"));
						notify(player, generate_json(
							["id" -> id, "result" -> "loggedin"]));
						return result;
					endif
				except e (ANY)
					result["result"] = "internalerror";
					result["errorcode"] = e[1];
					result["errormessage"] = e[2];
					result["errorvalue"] = e[3];
					result["errortraceback"] = e[4];
				endtry
			endif
		endif
	endif
	result["id"] = id;
	notify(player, generate_json(result));
.

;$verb($jsonserver, "do_command", $god)
program $jsonserver:do_command
	$restrict_to_server();
	
	if (argstr == "")
		return 1;
	endif
		
	s = `parse_json(argstr) ! ANY => $nothing';
	id = `s["id"] ! ANY => 0';
	result = ["result" -> "malformed"];
	if (typeof(s) == MAP)
		command = `s["command"] ! ANY => 0';
		if (typeof(command) == STR)
			command = tostr("cmd_", command);
			if (respond_to(player, command))
				try
					result = player:(command)(s);
				except e (ANY)
					result["result"] = "internalerror";
					result["errorcode"] = e[1];
					result["errormessage"] = e[2];
					result["errorvalue"] = e[3];
					result["errortraceback"] = e[4];
				endtry
			endif
		endif
	endif
	result["id"] = id;
	notify(player, generate_json(result));
	
	return 1;
.

;$verb($jsonserver, "user_connected", $god)
program $jsonserver:user_connected
.

;$verb($jsonserver, "user_created", $god)
program $jsonserver:user_created
	server_log(tostr("Player ", player.name, " (", player, ") created"));
	this:user_connected(player);
.

;$verb($jsonserver, "user_reconnected", $god)
program $jsonserver:user_reconnected
	server_log(tostr("Player ", player.name, " (", player, ") reconnected"));
	this:user_connected(player);
.

;$verb($jsonserver, "logincmd_connect", $god)
program $jsonserver:logincmd_connect
	$private();
	{message} = args;
	username = `message["username"] ! E_RANGE => 0';
	password = `message["password"] ! E_RANGE => 0';
	if ((typeof(username) != STR) || (typeof(password) != STR))
		return $nothing;
	endif
	
	try
		r = $authenticate(username, password);
		if (r == $nothing)
			return "authfailed";
		endif
		return r;
	except e (ANY)
		this:_log_error(e);
		return ["result" -> "authfailed"];
	endtry
.

;$verb($jsonserver, "logincmd_createplayer", $god)
program $jsonserver:logincmd_createplayer
	$private();
	{message} = args;
	
	username = `message["username"] ! E_RANGE => 0';
	password = `message["password"] ! E_RANGE => 0';
	server_log(tostr("login attempt by ", username)); 
	if ((typeof(username) != STR) || (typeof(password) != STR))
		return $nothing;
	endif
	
	server_log(generate_json(verbs($user)));
	r = $user:("create_player")(username, password);
	if (r == $nothing)
		return "creationfailed";
	endif
	return r;
.

# Player server commands.

# Start server on system start.

program $kernel:server_started
	$jsonserver.connection = listen($jsonserver, 7778, 0);
.

