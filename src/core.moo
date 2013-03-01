;add_property($system, "verb", $god, {$god, "r"})
;add_verb($system, {$god, "rxd", "verb"}, {"this", "none", "this"})
program $system:verb
	{object, name, owner, ?permissions="rxd"} = args;
	
	try
		delete_verb(object, name);
	except e (ANY)
	endtry
	
	add_verb(object, {owner, permissions, name}, {"this", "none", "this"});
.
