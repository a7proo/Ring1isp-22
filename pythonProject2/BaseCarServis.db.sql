BEGIN TRANSACTION;
DROP TABLE IF EXISTS "auto";
CREATE TABLE IF NOT EXISTS "auto" (
	"id"	INTEGER NOT NULL,
	"model"	TEXT NOT NULL,
	"marka"	TEXT NOT NULL,
	"Color"	TEXT NOT NULL,
	"Year_building"	INTEGER NOT NULL,
	"Number"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Services";
CREATE TABLE IF NOT EXISTS "Services" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "zakaz";
CREATE TABLE IF NOT EXISTS "zakaz" (
	"id"	INTEGER NOT NULL,
	"id_custemer"	INTEGER,
	"id_services"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_custemer") REFERENCES "customer"("id"),
	FOREIGN KEY("id_services") REFERENCES "Services"("id")
);
DROP TABLE IF EXISTS "customer";
CREATE TABLE IF NOT EXISTS "customer" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"surname"	TEXT NOT NULL,
	"num_phone"	INTEGER NOT NULL,
	"id_auto"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_auto") REFERENCES "auto"("id")
);
INSERT INTO "auto" ("id","model","marka","Color","Year_building","Number") VALUES (1,'Lada','Granta','Черный',2020,'аи456a'),
 (2,'BMW','X3','Белый',2000,'вы566B'),
 (3,'Toyota','Prius','Черный',2010,'pn876a'),
 (4,'Volkswagen','Passat','Белый',2015,'an893п'),
 (5,'Lada','Нива','Белый',2014,'шд584л'),
 (6,'Volkswagen','Golf','Черный',2021,'an563п'),
 (7,'Lada','Largus','Красный',2013,'ук466р'),
 (8,'Lada','Kalina','Синий',2021,'пр001п'),
 (9,'Lada','Kalina','Белый',2022,'см456м'),
 (10,'Lada','Race','Фиолетовый',2013,'пу228п'),
 (11,'BMW','Coupe','Черный',2007,'вв459B'),
 (12,'Toyota','Prius','Белый',2010,'пр457н'),
 (13,'Volkswagen','Prius','Белый','Фиолетовый','вр826й'),
 (14,'BMW','X5','Белый','Красный','ап284х'),
 (15,'Lada','Polo','Белый','Жёлтый','ий333й');
INSERT INTO "Services" ("id","name","price") VALUES (1,'Замена дисков',3800.0),
 (2,'Замена поршней в двигаделе',10800.0),
 (3,'Переобуть машину',5990.0),
 (4,'Слить масло',2000.0),
 (5,'Перепрошить компьютер',8900.0),
 (6,'Сменить замки на дверях',18000.0);
INSERT INTO "zakaz" ("id","id_custemer","id_services") VALUES (1,1,1),
 (2,2,2),
 (3,3,5),
 (4,4,4),
 (5,5,2),
 (6,6,1),
 (7,7,3),
 (8,8,3),
 (9,9,1),
 (10,10,1),
 (11,11,6),
 (12,12,3),
 (13,13,4),
 (14,14,2),
 (15,15,1);
INSERT INTO "customer" ("id","name","surname","num_phone","id_auto") VALUES (1,'Егор','Старостович',8976305455,4),
 (2,'Фиреро','Рафоэло',8247543298,12),
 (3,'Артур','Тигранович',8976483612,1),
 (4,'Азамат','Айталивев',8976483612,2),
 (5,'Азамат','Стетхем',8900846738,5),
 (6,'Макс','Максбетов',8990007654,3),
 (7,'Джо','Барбариска',8976329109,10),
 (8,'Юля','Штырицкая',8939481084,8),
 (9,'Тихон','Ероплк',8903194578,6),
 (10,'Анджела','Анимэв',8944522690,13),
 (11,'Юра','Бумперво',8956031958,11),
 (12,'Апостол','Завет',8934716851,7),
 (13,'Ира','Шрёдингер',8965345209,14),
 (14,'Грегорий','Малинов',8976400921,15),
 (15,'Грегорий','Грагасов',8965412334,9);
COMMIT;
