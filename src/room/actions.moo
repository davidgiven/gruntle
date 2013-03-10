;$verb($room, "actions", $god)
program $room:actions
	if (this:istemplate())
		return this.actions;
	else
		actions = [];
		for action, id in (this.actions)
			actions[id] =
				[
					"description" -> action["description"],
					"type" -> `action["type"] ! ANY => "room"',
					"target" -> action["target"]
				];
		endfor
		return actions;
	endif
.
