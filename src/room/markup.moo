;$verb($room, "markup", $god)
program $room:markup
	return
		[
			"type" -> "room",
			"name" -> this.name,
			"title" -> this.title,
			"oid" -> this:template()
		];
.
