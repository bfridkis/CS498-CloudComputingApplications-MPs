mysql -h database-1-mp6.cluster-cdaace60ubjw.us-east-1.rds.amazonaws.com -P 3306 -u admin -p

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