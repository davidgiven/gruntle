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
	
	r = $player:create_player(username, password);
	if (r == $nothing)
		return "creationfailed";
	endif
	return r;
.
