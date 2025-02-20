--set the output format of the result set to TSV (Tab-Separated Values) to compare the query results obtained, with the autograder.
--Make sure to leave the following line as the first line of your final solution!
!outputformat tsv

CREATE VIEW "powers" ( ROWKEY VARCHAR PRIMARY KEY, "personal"."hero" VARCHAR, "personal"."power" VARCHAR, "professional"."name" VARCHAR, "professional"."xp" VARCHAR, "custom"."color" VARCHAR ) ;

SELECT t1."name" AS "Name1", t2."name" AS "Name2", t1."power" AS "Power" FROM "powers" AS t1
JOIN "powers" as t2 ON t1."power" = t2."power" 
WHERE  t1."hero" = 'yes'
AND t2."hero" = 'yes';
-- AND t1."name" != t2."name";

-- REFERENCES
-- https://phoenix.apache.org/
-- https://phoenix.apache.org/faq.html#How_I_map_Phoenix_table_to_an_existing_HBase_table
-- https://community.cloudera.com/t5/Support-Questions/Views-on-existing-HBase-namespace-tables/td-p/167688
-- https://khodeprasad.wordpress.com/2016/07/26/how-to-use-existing-hbase-table-in-apache-phoenix/
-- https://lists.apache.org/thread/o0l9nnjgxd0s7lpchyo1qz99nhph9p3o
-- https://stackoverflow.com/questions/47075782/phoenix-convert-string-column-to-integer-column

-- Useful Phoenix shell commands:
-- !connect jdbc:phoenix:127.0.0.1:2181
-- !connect -p driver org.apache.phoenix.jdbc.PhoenixDriver -p user "none" -p password "none" "jdbc:phoenix:127.0.0.1:2181"
-- !help
-- !close