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
	result = ["event" -> "malformed"];
	if (typeof(s) == MAP)
		command = `s["command"] ! ANY => 0';
		if (typeof(command) == STR)
			command = tostr("logincmd_", command);
			if (respond_to(this, command))
				try
					r = this:(command)(s);
					if ((typeof(r) == OBJ) && (r != $nothing))
						notify(player, generate_json(
							[
								"id" -> id,
								"event" -> "loggedin",
								"user" -> r.name,
								"uid" -> r
							]
						));
						return r;
					endif
				except e (ANY)
					result["event"] = "internalerror";
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
