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
		if (r == $failed_match)
			return "authfailed";
		endif
		server_log(generate_json(r));
		return r;
	except e (ANY)
		this:_log_error(e);
		return ["result" -> "authfailed"];
	endtry
.
