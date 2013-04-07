PRAGMA auto_vacuum = FULL;
PRAGMA encoding = "UTF-8";
PRAGMA synchronous = OFF;
PRAGMA foreign_keys = ON;
PRAGMA temp_store = MEMORY;

-- Create the database schema.

CREATE TABLE variables
(
	key TEXT NOT NULL PRIMARY KEY,
	value TEXT
);

CREATE TABLE players
(
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE COLLATE NOCASE,
	email TEXT,
	password TEXT,
	connected INTEGER,
	instance INTEGER REFERENCES instances(id),
	room INTEGER REFERENCES rooms(id)
);
CREATE INDEX players_byusername ON players(username);
CREATE INDEX players_byinstance ON players(instance);
CREATE INDEX players_byroom ON players(room);

CREATE TABLE guests
(
	player INTEGER REFERENCES player(id)
);

CREATE TABLE realms
(
	id INTEGER PRIMARY KEY,
	owner INTEGER REFERENCES players(id),
	name TEXT
);
CREATE INDEX realms_byowner ON realms(owner);

CREATE TABLE instances
(
	id INTEGER PRIMARY KEY,
	realm INTEGER REFERENCES realms(id)
);
CREATE INDEX instances_byrealm ON instances(realm);

CREATE TABLE rooms
(
	id INTEGER PRIMARY KEY,
	realm INTEGER REFERENCES realms(id),
	name TEXT,
	title TEXT,
	description TEXT,
	actions BLOB,
	immutable INTEGER
);
CREATE INDEX rooms_byrealm ON rooms(realm);
CREATE INDEX rooms_byrealmname ON rooms(realm, name);

fnord;

-- Create Thoth and the default realm and instance.

INSERT INTO players (username, email, password, connected)
	VALUES ("Thoth", "<invalid>", "testpassword", 0);

INSERT INTO realms (owner, name)
	VALUES (
		(SELECT id FROM players WHERE username='Thoth'),
		"The Hub"
	);

INSERT INTO rooms (realm, name, title, description, immutable)
	VALUES (
		(SELECT id FROM realms WHERE name='The Hub'),
		'entrypoint',
		'Boring Nothingness',
		"It's very dull here.",
		1
	);

INSERT INTO instances (realm)
	VALUES (
		(SELECT id FROM realms LIMIT 1)
	);

UPDATE players SET
	instance = (SELECT id FROM instances LIMIT 1),
	room = (SELECT id FROM rooms LIMIT 1);

