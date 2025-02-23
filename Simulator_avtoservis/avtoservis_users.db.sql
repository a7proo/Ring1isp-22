BEGIN TRANSACTION;
DROP TABLE IF EXISTS "users";
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"login"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "users" ("id","login","password") VALUES (0,'master1','pas1'),
 (1,'master1','pas1'),
 (2,'master2','pas2'),
 (3,'admin','root'),
 (4,'manager','man123'),
 (5,'master3','pas3');
COMMIT;
