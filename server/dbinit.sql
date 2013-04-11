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
	name TEXT,
	owner INTEGER REFERENCES players(id)
);
CREATE INDEX realms_byowner ON realms(owner);

CREATE TABLE instances
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	realm INTEGER REFERENCES realms(id)
);
CREATE INDEX instances_byrealm ON instances(realm);

-- Rooms.
 
CREATE TABLE rooms
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	title TEXT,
	description TEXT,
	actions BLOB,
	immutable INTEGER,
	realm INTEGER REFERENCES realms(id)
);
CREATE INDEX rooms_byname ON rooms(name);
CREATE INDEX rooms_byrealm ON rooms(realm);

-- Actions.

CREATE TABLE actions
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description TEXT,
	type TEXT,
	target TEXT,
	room INTEGER REFERENCES rooms(id)
);
CREATE INDEX actions_byroom ON actions(room);
	
COMMIT;
