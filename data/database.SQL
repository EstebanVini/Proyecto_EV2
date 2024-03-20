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

