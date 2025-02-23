BEGIN TRANSACTION;
DROP TABLE IF EXISTS "tovar";
CREATE TABLE IF NOT EXISTS "tovar" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"price"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "tovar_buy";
CREATE TABLE IF NOT EXISTS "tovar_buy" (
	"id"	INTEGER,
	"id_tovar"	INTEGER,
	"price"	REAL,
	"kol"	INTEGER,
	"sum"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_tovar") REFERENCES "tovar"("id") ON DELETE CASCADE
);
DROP TABLE IF EXISTS "tovar_sell";
CREATE TABLE IF NOT EXISTS "tovar_sell" (
	"id"	INTEGER,
	"id_tovar"	INTEGER,
	"price"	REAL,
	"kol"	INTEGER,
	"sum"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_tovar") REFERENCES "tovar"("id") ON DELETE CASCADE
);
INSERT INTO "tovar" ("id","name","price") VALUES (2,'Шины летние 4шт.',2000.0),
 (3,'Шины зимние 4шт.',3000.0),
 (4,'Двигатель в сборе',10000.0),
 (5,'Моторное масло',1000.0),
 (6,'Дворники',800.0),
 (7,'Свеча зажигания',1000.0),
 (8,'Бампер ',1000000.0);
INSERT INTO "tovar_buy" ("id","id_tovar","price","kol","sum") VALUES (1,3,3000.0,6,18000.0),
 (2,6,800.0,14,11200.0);
COMMIT;
