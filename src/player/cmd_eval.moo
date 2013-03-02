;$verb($player, "cmd_eval", $god)
program $player:cmd_eval
	set_task_perms(this);
	{message} = args;
	
	expr = `message["code"] ! E_RANGE => "0"';
	result = eval(expr);
	return ["result"->"eval", "value"->result];
.
