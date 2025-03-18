scheduled_arrival = 603+2400
scheduled_departure = 1840
scheduled_time = 443

(int(scheduled_arrival / 100)*60 + \
(scheduled_arrival % 100) - (int(scheduled_departure / 100)*60 + \
(scheduled_departure % 100) + scheduled_time))%(24*60)

(int(scheduled_arrival / 100)*60 + (scheduled_arrival % 100) - (int(scheduled_departure / 100)*60 + (scheduled_departure % 100) + scheduled_time))%(24*60)

spark_df_w_time_zone_difference.filter((col("scheduled_arrival") < col("scheduled_departure")) & (col("scheduled_departure") - col("scheduled_arrival") >= 1200)).select("scheduled_arrival", "scheduled_departure", "scheduled_time", "time_zone_difference").show(10)
spark_df_w_time_zone_difference.filter((col("scheduled_arrival") < col("scheduled_departure"))).select("scheduled_arrival", "scheduled_departure", "scheduled_time", "time_zone_difference").show(10)

spark_df_w_time_zone_difference.filter(col('time_zone_difference') < 0).select('scheduled_arrival', 'scheduled_departure', 'scheduled_time', 'time_zone_difference').show(10)

spark_df_w_time_zone_difference.agg({'time_zone_difference':'max'}).show()