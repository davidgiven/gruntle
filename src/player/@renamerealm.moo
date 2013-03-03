;$verb($player, "@renamerealm", $god, "rx")
;set_verb_args($player, "@renamerealm", {"any", "none", "none"});
program $player:@renamerealm
	set_task_perms(this);
	realm = player.location:realm();
	if (realm.owner != player)
		notify(player, "You don't own this realm.");
		return;
	endif
	
	realm:rename(argstr);
.
