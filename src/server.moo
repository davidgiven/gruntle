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
	set_connection_option(player, "hold-input", 1);
	
	while (1)
		s = read(player);
		s = `parse_json(s) ! ANY => $nothing';
		id = `s["id"] ! ANY => 0';
		result = ["result" -> "malformed"];
		if (typeof(s) == MAP)
			command = `s["command"] ! ANY => 0';
			if (typeof(command) == STR)
				command = tostr("logincmd_", command);
				if (respond_to(this, command))
					result = this:(command)(s);
					if ((typeof(result) == OBJ) && (result != $nothing))
						server_log(tostr("player ", result.name, " logged in"));
						notify(player, generate_json(
							["id" -> id, "result" -> "loggedin"]));
						return result;
					elseif (typeof(result) == MAP)
						break;
					else
						continue;
					endif
				endif
			endif
		endif
		result["id"] = id;
		notify(player, generate_json(result));
	endwhile
.

;$verb($jsonserver, "logincmd_connect", $god)
program $jsonserver:logincmd_connect
	$private();
	{message} = args;
	username = `message["username"] ! E_RANGE => 0';
	password = `message["password"] ! E_RANGE => 0';
	server_log(tostr("login attempt by ", username)); 
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
	
	try
		r = $createplayer(username, password);
		if (r == $nothing)
			return "creationfailed";
		endif
		return r;
	except e (ANY)
		this:_log_error(e);
		return ["result" -> "creationfailed"];
	endtry
.

# Start server on system start.

program $kernel:server_started
	$jsonserver.connection = listen($jsonserver, 7778, 0);
.

