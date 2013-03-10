# General server settings.

;$welcome_message = "If you don't know what to do here, you shouldn't be here."
;$disable_passkey_login = 1
;$player.salt = tostr("$1$", random())

# Create the special realm god lives in.

;;
	realm = $god:create_realm("Godworld");
	instance = realm:create_instance();
	
	r = realm:find_room_template("entrypoint");
	r.title = "Heaven";
	r.description = "Harps, clouds and cherubim as far as the eye can see.";
	
	move($god, instance:find_room("entrypoint"));
.

# Create the default realm, which belongs to Thoth.

;$property($system, "defaultrealm", $god)
;$property($system, "defaultinstance", $god)

;$defaultrealm = $thoth:create_realm("The Hub")
;$defaultinstance = $defaultrealm:create_instance()

;;
	r = $defaultrealm:find_room_template("entrypoint");
	r.title = "Centre of the Universe";
	r.description = tostr(
		"An infinite, perfectly flat plain of dull grey stretches out ",
		"beneath a dull grey sky. It looks incredibly generic. The only ",
		"interesting feature is a stairwell leading down into darkness, and ",
		"a small yellow sign marked 'Under Construction'.");
	
	r:addaction("Follow the stairwell down", "room", "storeroom");
.

;;
	r = $defaultrealm:create_room("storeroom");
	r.title = "Cluttered storeroom";
	r.description = tostr(
		"It's dark here and you keep tripping over things. The only thing ",
		"that's even slightly interesting to do here is to head back up ",
		"the stairs.");
		
	r:addaction("Return back up the stairs", "room", "entrypoint");
.

# ...set up god and Thoth.

;$god.name = "God"
;$god:change_password("testpassword")

;$thoth:change_password("testpassword")
;move($thoth, $defaultinstance:find_room("entrypoint"))
