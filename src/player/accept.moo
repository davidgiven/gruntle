;$verb($player, "accept", $god)
program $player:accept
	{o} = args;
	return ($realm in parents(o)) && (o.owner == this);
.
