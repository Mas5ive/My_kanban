BEGIN TRANSACTION;
DROP TABLE IF EXISTS "board";
CREATE TABLE "board" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "user";
CREATE TABLE  "user" (
	"name"	    TEXT,
	"psw_hash"	TEXT NOT NULL,
	PRIMARY KEY("name")
);
DROP TABLE IF EXISTS "comment";
CREATE TABLE "comment" (
	"id"	    INTEGER,
	"author"	TEXT    NOT NULL,
	"card_id"	INTEGER NOT NULL,
	"content"	TEXT    NOT NULL,
	"date"	    TEXT    NOT NULL,
	FOREIGN KEY("card_id") REFERENCES "card"("id")   ON DELETE CASCADE,
	FOREIGN KEY("author")  REFERENCES "user"("name") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "invitation";
CREATE TABLE "invitation" (
	"user_recipient" TEXT,
	"board_id"	     INTEGER,
	"user_sender"	 TEXT         NOT NULL CHECK("user_sender" <> "user_recipient"),
	FOREIGN KEY("board_id")       REFERENCES "board"("id")  ON DELETE CASCADE,
	FOREIGN KEY("user_sender")    REFERENCES "user"("name") ON DELETE CASCADE,
	FOREIGN KEY("user_recipient") REFERENCES "user"("name") ON DELETE CASCADE,
	PRIMARY KEY("user_recipient","board_id")
);
DROP TABLE IF EXISTS "user_board";
CREATE TABLE "user_board" (
	"username"	TEXT      NOT NULL,
	"board_id"	INTEGER   NOT NULL,
	"is_owner"	INTEGER   DEFAULT 0,
	FOREIGN KEY("board_id") REFERENCES "board"("id")  ON DELETE CASCADE,
	FOREIGN KEY("username") REFERENCES "user"("name") ON DELETE CASCADE,
	PRIMARY KEY("username","board_id")
);
DROP TABLE IF EXISTS "card";
CREATE TABLE "card" (
	"id"	    INTEGER,
	"board_id"	INTEGER NOT NULL,
	"title"	    TEXT    NOT NULL,
	"content"	TEXT,
	"status"	INTEGER DEFAULT 0,
	FOREIGN KEY("board_id") REFERENCES "board"("id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "board" VALUES (1,'Amazing project');
INSERT INTO "board" VALUES (2,'Boring project');
INSERT INTO "board" VALUES (3,'My project');
INSERT INTO "user" VALUES ('demo_user','scrypt:32768:8:1$LDgFbOM6J4koR5n6$341af5b066c81a6326f2da889d52eac60fa6ca6001ec9d0325a21cf63cc0a3be68e2c586c4132e5097e305c67c8e01d28594b695f7ba441cd97d4f9f52e4d500');
INSERT INTO "user" VALUES ('user1','scrypt:32768:8:1$8jKDHimugevfQH8r$e7181dc14e4265cfac91617134895b53fd5df025585a838c6e36d33dcee4821b853b8b6ec26176441772473fadcbe050e76fb9010c97642a120d28261ac446eb');
INSERT INTO "user" VALUES ('user2','scrypt:32768:8:1$cLUT099toyv3kx2W$053838394d6b2c02f260d3cc3aa5b5b25c06819c649a2e728a7288c29ff95a0ce7ef67cea3ac9faa612995fae2e0b7e3542f19aa7cfd3b2dd0db95345859d223');
INSERT INTO "user_board" VALUES ('user1',1,1);
INSERT INTO "user_board" VALUES ('user2',2,1);
INSERT INTO "user_board" VALUES ('demo_user',3,1);
INSERT INTO "user_board" VALUES ('user1',3,0);
INSERT INTO "user_board" VALUES ('user2',3,0);
INSERT INTO "card" VALUES (1,3,'Build a four-story house of cards','The house should be in classicism style.',1);
INSERT INTO "card" VALUES (2,3,'Choose furniture for a house of cards','Try to choose furniture that matches the color of the cards. I don''t like bad taste.',0);
INSERT INTO "card" VALUES (3,1,'Create a jet pack',NULL,2);
INSERT INTO "card" VALUES (4,2,'Invent a transport vehicle on two wheels',NULL,0);
INSERT INTO "comment" VALUES (1,'user1',1,'I swear that yesterday I built 3/4 of this house, but the wind blew it all away!','2024-01-30 12:00:00');
INSERT INTO "comment" VALUES (2,'demo_user',1,'This is simply impossible. You can''t do it because you''re lazy. Just try not to sleep. I believe in you!','2024-01-30 12:10:00');
INSERT INTO "comment" VALUES (3,'user2',2,'I know an excellent furniture store. But wait... for a house of cards???','2024-01-30 14:00:00');
INSERT INTO "comment" VALUES (4,'demo_user',2,'It will be four floors, so everything is fine. It should fit. Let me know how you choose the right options.','2024-01-30 14:15:00');
INSERT INTO "invitation" VALUES ('demo_user',1,'user1');
INSERT INTO "invitation" VALUES ('demo_user',2,'user2');
COMMIT;
