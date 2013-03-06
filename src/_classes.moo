;$class("player", "Generic Player", $nothing)
;chparent($god, $player)

# Special players.

;$class("guest", "Generic Guest", $player)
;$class("thoth", "Thoth", $player)
;set_player_flag($thoth, 1)

;$class("realm", "Generic Realm", $nothing);
;$class("room", "Generic Room", #7);
;$class("jsonserver", "JSON Network Server", $nothing);
