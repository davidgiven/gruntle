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
	if (typeof(result) == MAP)
		result["id"] = id;
		player:tell(result);
	endif
	
	return 1;
.
