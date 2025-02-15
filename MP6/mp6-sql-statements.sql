mysql -h database-1-mp6.cluster-cdaace60ubjw.us-east-1.rds.amazonaws.com -P 3306 -u admin -p;
USE mp6_db;

CREATE TABLE mp6_table1 (
    `id` INTEGER unsigned AUTO_INCREMENT,
    `name` VARCHAR(20),
    `hero` VARCHAR(20),
    `power` VARCHAR(20),
    `xp` INTEGER unsigned,
    `color` VARCHAR(20),
    PRIMARY KEY (`id`)
);

LOAD DATA FROM S3 's3://mp6-bucket-fridkis2/mp6data.csv' 
INTO TABLE mp6_table1
FIELDS TERMINATED BY ','
IGNORE 1 LINES;

SELECT * FROM mp6_table1 ORDER BY name LIMIT 10;

INSERT INTO mp6_table1 (`hero`, `power`, `name`, `xp`, `color`) VALUES ("yes", "fire", "fireman", "1000001", "red");
INSERT INTO mp6_table1 (`hero`, `power`, `name`, `xp`, `color`) VALUES ("no", "bark", "dogman", "1000001", "brown");
SELECT * FROM mp6_table1 WHERE xp = 1000001 or xp = 1000002;
SELECT * FROM mp6_table1 WHERE id > 1000000;
DELETE FROM mp6_table1 WHERE id > 1000000;
ALTER TABLE mp6_table1 AUTO_INCREMENT=1000001;

TRUNCATE TABLE mp6_table1;
