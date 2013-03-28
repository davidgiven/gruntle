;$verb($script, "_create_tokeniser", $god)
program $script:_create_tokeniser
	$private();
	{source} = args;

	t = create($nothing, 1);
	
	$property(t, "source", $god);
	t.source = source;
	
	$property(t, "current", $god);
	t.current = "";

	$property(t, "line", $god);
	t.line = 0;
	
	$property(t, "column", $god);
	t.column = 0;
	
	return t;
.
