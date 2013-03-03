;$verb($player, "cmd_eval", $god)
program $player:cmd_eval
	set_task_perms(caller_perms());
	{message} = args;
	
	expr = `message["code"] ! E_RANGE => "0"';
	result = eval(expr);
	return ["event"->"eval", "value"->result];
.
