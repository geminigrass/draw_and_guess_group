PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
-- CREATE TABLE wedraw_tableword(wordId  INT PRIMARY KEY NOT NULL, wordfield VARCHAR(30) NOT NULL, word VARCHAR(30) NOT NULL);
INSERT INTO "wedraw_tableword" VALUES(1,'IT','bitcoin','bit','coin','bitcoin');
INSERT INTO "wedraw_tableword" VALUES(2,'IT','webapp','web','app','webapp');
INSERT INTO "wedraw_tableword" VALUES(3,'food','apple','fruit','app','apple');
INSERT INTO "wedraw_tableword" VALUES(4,'human','hand','human','body','hand');
INSERT INTO "wedraw_controller" VALUES(1,0,0,'000');
COMMIT;
