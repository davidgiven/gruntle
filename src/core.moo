;add_verb($system, {$god, "rxd", "verb"}, {"this", "none", "this"})
program $system:verb
	set_task_perms(caller_perms());
	{object, name, owner, ?permissions="rxd"} = args;
	
	try
		delete_verb(object, name);
	except e (ANY)
	endtry
	
	add_verb(object, {owner, permissions, name}, {"this", "none", "this"});
.

;$verb($system, "property", $god)
program $system:property
	set_task_perms(caller_perms());
	{object, name, owner, ?permissions="rc"} = args;
	
	try
		set_property_info(object, name, {owner, permissions});
	except e (ANY)
		add_property(object, name, $nothing, {owner, permissions});
	endtry
.

;$verb($system, "class", $god)
program $system:class
	$permit("wizard");
	{name, description, parents} = args;
	
	if (name in properties($system))
		o = $system.(name);
		chparents(o, parents);
	else
		o = create(parents, $god);
		$property($system, name, $god);
		$system.(name) = o;
	endif
	o.name = description;
.
