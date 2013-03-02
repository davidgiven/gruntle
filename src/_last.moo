# General server settings.

;$welcome_message = "If you don't know what to do here, you shouldn't be here."
;$disable_passkey_login = 1

# Create the default realm, which belongs to god.

;$property($system, "defaultrealm", $god)
;$property($system, "defaultinstance", $god)

;$defaultrealm = $god:create_realm("The Hub")
;$defaultinstance = $defaultrealm:create_instance()

;$defaultrealm:find_room_template("entrypoint").description = "An infinite, perfectly flat plain of dull grey stretches out beneath a dull grey sky."

# ...set up god.

;$god.name = "God"
;$god.password = crypt("testpassword", $player.salt)
