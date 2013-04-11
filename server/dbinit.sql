PRAGMA auto_vacuum = FULL;
PRAGMA encoding = "UTF-8";
PRAGMA synchronous = OFF;
PRAGMA foreign_keys = ON;
PRAGMA temp_store = MEMORY;

BEGIN;

-- Global settings.

CREATE TABLE variables
(
	key TEXT NOT NULL PRIMARY KEY,
	value TEXT
);

-- Players, and player-related stuff.

CREATE TABLE players
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE COLLATE NOCASE,
	email TEXT,
	password TEXT,
	connected INTEGER,
	guest INTEGER,
	instance INTEGER REFERENCES instances(id),
	room INTEGER REFERENCES rooms(id)
);
CREATE INDEX players_byname ON players(name);
CREATE INDEX players_byroom ON players(room);
CREATE INDEX players_byinstance ON players(instance);
CREATE INDEX players_byguest ON players(guest);

-- Realms and instances.

CREATE TABLE realms
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT
);

CREATE TABLE instances
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	realm INTEGER REFERENCES realms(id)
);
CREATE INDEX instances_byrealm ON instances(realm);

CREATE TABLE realms_in_player
(
	player INTEGER REFERENCES players(id) ON DELETE CASCADE,
	realm INTEGER REFERENCES realms(id) ON DELETE CASCADE
);
CREATE INDEX realms_in_player_byplayer ON realms_in_player(player);
CREATE INDEX realms_in_player_byinstance ON realms_in_player(realm);

-- Rooms.
 
CREATE TABLE rooms
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	title TEXT,
	description TEXT,
	actions BLOB,
	immutable INTEGER
);
CREATE INDEX rooms_bymname ON rooms(name);

CREATE TABLE rooms_in_realm
(
	realm INTEGER REFERENCES realms(id) ON DELETE CASCADE,
	room INTEGER REFERENCES rooms(id) ON DELETE CASCADE
);
CREATE INDEX rooms_in_realm_byrealm ON rooms_in_realm(realm);
CREATE INDEX rooms_in_realm_byroom ON rooms_in_realm(room);

-- Actions.

CREATE TABLE actions
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description TEXT,
	type TEXT,
	target TEXT
);

CREATE TABLE actions_in_room
(
	action INTEGER REFERENCES actions(id) ON DELETE CASCADE,
	room INTEGER REFERENCES rooms(id) ON DELETE CASCADE
);
CREATE INDEX action_in_room_byaction ON actions_in_room(action);
CREATE INDEX action_in_room_byroom ON actions_in_room(room);
	
COMMIT;
