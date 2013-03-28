;$verb($script, "_token", $god)
program $script:_token
	$private();
	{t} = args;

	c = t.current;
	if (c == $nothing)
		/* End of file. */
		return {"eof"};
	elseif (c == "")
		/* Empty line --- move on to the next one. */
		t.line = t.line + 1;
		t.column = 1;
		t.current = `t.source[t.line] ! E_RANGE => $nothing';
		
		/* ...and try again. */
		return this:_token(t);
	elseif (r = match(t.current, "^ +))
		/* There's leading white space on this line. Consume it. */
		end = r[2];
		t.column = t.column + end;
		t.current = t.current[end..$];
		
		/* Try again. */
		return this:_token(t);
	else
		/* Parse error. */
		return {"error",
			[
				"message" -> "parse error",
				"line" -> t.line,
				"column" -> t.column
			]
		};
	endif
.
