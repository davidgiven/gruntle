# Import the primitive Stunt package. (Actually gets deferred until the first
# time the DB is actually used.)

program $composed:import_package_from_file
  {filename} = args;
  server_log(tostr("importing package: ", filename));
  fh = -1;
  try
    fh = file_open(filename, "r-tn");
    data = file_read(fh, 1000000);
    file_close(fh);
    fh = -1;
    package = parse_json(data, "embedded-types");
    object = $composed:import(package);
    $composed:install(object);
  finally
    fh > -1 && file_close(fh);
  endtry
.

;$composed:import_package_from_file("primitive-0.0.4.json")

# Set up some system variables.

;add_property(#0, "god", #5, {#5, "r"})

# Useful tools which will be used later to create our objects.

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
