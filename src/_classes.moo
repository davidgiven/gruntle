;$class("player", "Generic Player", $nothing)
;chparent($god, $player)

# Special players.

;$class("guest", "Generic Guest", $player)
;$class("thoth", "Thoth", $player)
;set_player_flag($thoth, 1)
;$thoth.programmer = 1
;$thoth.owner = $thoth

;$class("realm", "Generic Realm", $nothing);
;$class("room", "Generic Room", #7);
;$class("jsonserver", "JSON Network Server", $nothing);

# The special room for logged off players.

;$property($system, "limbo", $god, "r")
;;
	if ($limbo == $nothing)
		$limbo = create($room, $god);
		$limbo.name = "Limbo";
	endif
.

# Scripting compiler.

;$class("script", "Scripting Compiler", $nothing);
