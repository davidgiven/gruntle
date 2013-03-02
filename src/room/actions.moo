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
					"target" -> action["target"]
				];
		endfor
		return actions;
	endif
.
