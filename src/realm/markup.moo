;$verb($realm, "markup", $god)
program $realm:markup
	if (this:checkrealm())
		return
			[
				"type" -> "realm",
				"name" -> this.name,
				"oid" -> this
			];
	else
		return
			[
				"type" -> "instance",
				"name" -> this.name,
				"oid" -> this
			];
	endif
.
