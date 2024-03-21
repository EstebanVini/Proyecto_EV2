CREATE TABLE "users" (
	"id"	INTEGER,
	"username"	TEXT,
	"email"	TEXT,
	"password"	TEXT,
	"salt"	TEXT,
	"relatedto"	TEXT,
	"admin"	BOOLEAN,
	PRIMARY KEY("id")
);


CREATE TABLE "messages" (
	"id"	INTEGER NOT NULL UNIQUE,
	"userID"	INTEGER,
	"sender"	TEXT,
	"receiver"	TEXT,
	"message"	TEXT,
	"date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("userID") REFERENCES "users"
);

INSERT INTO "messages" ("userID", "sender", "receiver", "message", "date") VALUES (2, "Esteban02", "Esteban", "Hello, how are you?", "2022-01-01");