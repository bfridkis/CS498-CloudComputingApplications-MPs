from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("LoadJSON").getOrCreate()

file_path = "C:\\Users\\Annjamin\\Documents\\Benj's Stuff\\UIUC MCS\\CS498-CloudComputingApplications\\CS498-CloudComputingApplications-MPs\\MP9\\Transformed-Output\\Glue-Job-1\\run-1742245204333-part-r-00000"
spark_df = spark.read.json(file_path)

max_travel_time = spark_df_w_time_zone_difference.agg({'scheduled_time':'max'}).collect()[0]['max(scheduled_time)']

#spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", when((col("scheduled_arrival") < col("scheduled_departure")) & (col("scheduled_departure") - col("scheduled_arrival") >= 1200), 
# spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", when((col("scheduled_arrival") < col("scheduled_departure")) & 
                                                                                   # ((((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time)) - \
                                                                                   # (((spark_df.scheduled_arrival+2400) / 100).cast('int')*60 + \
                                                                                   # ((spark_df.scheduled_arrival) % 100)) >= max_travel_time), 
                                                                                   # ((((spark_df.scheduled_arrival+2400) / 100).cast('int')*60 + \
                                                                                   # ((spark_df.scheduled_arrival) % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                             # .otherwise(((spark_df.scheduled_arrival / 100).cast('int')*60 + \
                                                                                        # (spark_df.scheduled_arrival % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                        # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                                        
# spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", when((col("scheduled_arrival") < col("scheduled_departure")) & 
                                                                                   # ((((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   # (spark_df.scheduled_departure % 100))) - \
                                                                                   # (((spark_df.scheduled_arrival) / 100).cast('int')*60 + \
                                                                                   # ((spark_df.scheduled_arrival) % 100)) > spark_df.scheduled_time), 
                                                                                   # ((((spark_df.scheduled_arrival+2400) / 100).cast('int')*60 + \
                                                                                   # ((spark_df.scheduled_arrival) % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                             # .otherwise(((spark_df.scheduled_arrival / 100).cast('int')*60 + \
                                                                                        # (spark_df.scheduled_arrival % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                        # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                                        
spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", when((col("scheduled_arrival") < col("scheduled_departure")) & 
                                                                                   (col("scheduled_time") >= 60), 
                                                                                   ((((spark_df.scheduled_arrival+2400) / 100).cast('int')*60 + \
                                                                                   ((spark_df.scheduled_arrival) % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                             .otherwise(((spark_df.scheduled_arrival / 100).cast('int')*60 + \
                                                                                        (spark_df.scheduled_arrival % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                        (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))

spark_df_w_time_zone_difference.filter((col("scheduled_arrival") < col("scheduled_departure")) & (col("scheduled_departure") - col("scheduled_arrival") >= 1200)).select("scheduled_arrival", "scheduled_departure", "scheduled_time", "time_zone_difference").show(10)
spark_df_w_time_zone_difference.filter((col("scheduled_arrival") < col("scheduled_departure"))).select("scheduled_arrival", "scheduled_departure", "scheduled_time", "time_zone_difference").show(10)

spark_df_w_time_zone_difference.filter(col('time_zone_difference') < 0).select('scheduled_arrival', 'scheduled_departure', 'scheduled_time', 'time_zone_difference').show(10)

spark_df_w_time_zone_difference.agg({'scheduled_time':'max'}).show()
spark_df_w_time_zone_difference.agg({'time_zone_difference':'max'}).show()
spark_df_w_time_zone_difference.agg({'time_zone_difference':'max'}).show()

scheduled_arrival = 630+2400
scheduled_departure = 629
scheduled_time = 59

(int(scheduled_arrival / 100)*60 + \
(scheduled_arrival % 100) - (int(scheduled_departure / 100)*60 + \
(scheduled_departure % 100) + scheduled_time))%(24*60)

(int(scheduled_arrival / 100)*60 + (scheduled_arrival % 100) - (int(scheduled_departure / 100)*60 + (scheduled_departure % 100) + scheduled_time))%(24*60)