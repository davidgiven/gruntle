;$verb($script, "compile", $god)
program $script:compile
	{source, owner} = args;
	
	tokeniser = this:_create_tokeniser(source);
	{output, errorlog} = this:_compile(tokeniser);
	if (errorlog)
		raise(E_INVARG, "Compilation error", errorlog);
	endif
	
	newobj = create($script, 1);
	add_verb(newobj, {$owner, "rxd", "run"}, {"this", "none", "this"});
	set_verb_code(newobj, "run", output);
	
	return output;
.
