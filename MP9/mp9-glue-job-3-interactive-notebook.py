### mp9 - 3.2.3.1

## Get means pre-removal of duplicates
departure_delay_mean_w_duplicates = round(df.agg({'departure_delay':'avg'}).collect()[0]['avg(departure_delay)'])
#print("Departure Delay Mean with Duplicates:", departure_delay_mean_w_duplicates)
air_time_mean_w_duplicates = round(df.agg({'air_time':'avg'}).collect()[0]['avg(air_time)'])
#print("Air Time Mean with Duplicates:", air_time_mean_w_duplicates)
arrival_delay_mean_w_duplicates = round(df.agg({'arrival_delay':'avg'}).collect()[0]['avg(arrival_delay)'])
#print("Arrival Delay Mean with Duplicates:", arrival_delay_mean_w_duplicates)
## Get standard deviations pre-removal of duplicates
departure_delay_stddev_w_duplicates = round(df.agg({'departure_delay':'stddev'}).collect()[0]['stddev(departure_delay)'])
#print("Departure Delay Stddev with Duplicates:", departure_delay_stddev_w_duplicates)
air_time_stddev_w_duplicates = round(df.agg({'air_time':'stddev'}).collect()[0]['stddev(air_time)'])
#print("Air Time Stddev with Duplicates:", air_time_stddev_w_duplicates)
arrival_delay_stddev_w_duplicates = round(df.agg({'arrival_delay':'stddev'}).collect()[0]['stddev(arrival_delay)'])
#print("Arrival Delay Stddev with Duplicates:", arrival_delay_stddev_w_duplicates)

df_no_dups = df.dropDuplicates()

## Get means post-removal of duplicates
departure_delay_mean_wo_duplicates = round(df_no_dups.agg({'departure_delay':'avg'}).collect()[0]['avg(departure_delay)'])
#print("Departure Delay Mean without Duplicates:", departure_delay_mean_wo_duplicates)
air_time_mean_wo_duplicates = round(df_no_dups.agg({'air_time':'avg'}).collect()[0]['avg(air_time)'])
#print("Air Time Mean without Duplicates:", air_time_mean_wo_duplicates)
arrival_delay_mean_wo_duplicates = round(df_no_dups.agg({'arrival_delay':'avg'}).collect()[0]['avg(arrival_delay)'])
#print("Arrival Delay Mean without Duplicates:", arrival_delay_mean_wo_duplicates)
## Get standard deviations post-removal of duplicates
departure_delay_stddev_wo_duplicates = round(df_no_dups.agg({'departure_delay':'stddev'}).collect()[0]['stddev(departure_delay)'])
#print("Departure Delay Stddev without Duplicates:", departure_delay_stddev_wo_duplicates)
air_time_stddev_wo_duplicates = round(df_no_dups.agg({'air_time':'stddev'}).collect()[0]['stddev(air_time)'])
#print("Air Time Stddev without Duplicates:", air_time_stddev_wo_duplicates)
arrival_delay_stddev_wo_duplicates = round(df_no_dups.agg({'arrival_delay':'stddev'}).collect()[0]['stddev(arrival_delay)'])
#print("Arrival Delay Stddev without Duplicates:", arrival_delay_stddev_wo_duplicates)

num_duplicates = df.count() - df_no_dups.count()
total_change_for_mean = abs(departure_delay_mean_wo_duplicates - departure_delay_mean_w_duplicates) + abs(air_time_mean_wo_duplicates - air_time_mean_w_duplicates) + abs(arrival_delay_mean_wo_duplicates - arrival_delay_mean_w_duplicates)
total_change_for_stddev = abs(departure_delay_stddev_wo_duplicates - departure_delay_stddev_w_duplicates) + abs(air_time_stddev_wo_duplicates - air_time_stddev_w_duplicates) + abs(arrival_delay_stddev_wo_duplicates - arrival_delay_stddev_w_duplicates)

[num_duplicates, total_change_for_mean, total_change_for_stddev]

# https://www.google.com/search?q=how+to+get+column+mean+in+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=how+to+get+column+mean+in+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRigATIHCAQQIRigATIHCAUQIRiPAtIBCDUxMTZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# https://www.google.com/search?q=how+to+get+column+standard+deviation+in+pyspark&sca_esv=45c41d3e543101a5&rlz=1C1CHBF_enUS1071US1071&ei=fdTZZ96dEvrcwN4Pr6y7-QE&oq=how+to+get+column+stanin+pyspark&gs_lp=Egxnd3Mtd2l6LXNlcnAiIGhvdyB0byBnZXQgY29sdW1uIHN0YW5pbiBweXNwYXJrKgIIADIKECEYoAEYwwQYCjIKECEYoAEYwwQYCjIKECEYoAEYwwQYCjIKECEYoAEYwwQYCkjnI1D_Dli0GHADeAGQAQCYAb4BoAGmBqoBAzAuNbgBA8gBAPgBAZgCBqAC-gPCAgoQABiwAxjWBBhHwgIIEAAYBxgIGB7CAgYQABgNGB7CAggQABgIGA0YHsICCxAAGIAEGIYDGIoFwgIFEAAY7wWYAwCIBgGQBgiSBwMzLjOgB8UksgcDMC4zuAfnAw&sclient=gws-wiz-serp
# https://www.google.com/search?q=find+duplicates+py+spark+dataframe&rlz=1C1CHBF_enUS1071US1071&oq=find+duplicates+py+spark+dataframe&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCAgCEAAYFhgeMggIAxAAGBYYHjIICAQQABgWGB4yCAgFEAAYFhgeMg0IBhAAGIYDGIAEGIoFMg0IBxAAGIYDGIAEGIoFMgoICBAAGIAEGKIE0gEINjU5MGowajeoAgCwAgA&sourceid=chrome&ie=UTF-8

### mp9 - 3.2.3.2

from pyspark.sql.functions import concat_ws

df_w_route = df.withColumn("route", concat_ws("-", "origin_airport", "destination_airport"))
#df_w_route.groupby('route').agg({'Route':'count'}).sort('count(Route)', ascending=False).withColumnRenamed('count(Route)', 'count').show(10)
df_to_write = df_w_route.groupby('route').agg({'Route':'count'}).sort('count(Route)', ascending=False).withColumnRenamed('count(Route)', 'count').limit(10)

df_to_write.write.csv('s3://fridkis-mp9-flights-dataset/Submission-Output/TopTenRoutes', header=True, mode="overwrite")

# https://www.geeksforgeeks.org/how-to-add-a-new-column-to-a-pyspark-dataframe/
# https://www.google.com/search?q=group+by+py+spark&rlz=1C1CHBF_enUS1071US1071&oq=group+by+py+spark&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIKCAEQABgKGBYYHjIICAIQABgWGB4yCggDEAAYChgWGB4yCAgEEAAYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhgeMggICBAAGBYYHjIICAkQABgWGB7SAQg1NzY1ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
# https://www.google.com/search?q=rename+column+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=rename+column+pyspark&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBwgCEAAYgAQyBwgDEAAYgAQyCAgEEAAYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhgeMggICBAAGBYYHjINCAkQABiGAxiABBiKBdIBCDI4ODVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# https://www.google.com/search?num=12&sca_esv=45c41d3e543101a5&rlz=1C1CHBF_enUS1071US1071&q=write+dataframe+to+csv+pyspark+glue+notebook&source=lnms&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpTCgsr7ZAdxc8ed8cDHoFGnBBHvqR82JDXvFRVwuR0NNNtJH6THxpN4wQuXHLuZFM93gflBEkhcmLjZFKeuVDJ9I7dWmqJ-AuNazMuNgSFMJP-7RUncRzTCOmVe0nOkDLqtGzOhTay_WmOw6DefeVRrWqjklUaIs7a-cE4rsDnyf432Xby_1KUJkPqUojuBlB2DRgzg&sa=X&ved=2ahUKEwi4p9fIyJSMAxVB4zQHHSOkJVsQ0pQJegQIDRAB&biw=2560&bih=1214&dpr=0.75

### mp9 - 3.2.3.3

from pyspark.sql.functions import corr

dd_correlations = dict()

for col in ['scheduled_time', 'elapsed_time', 'diverted', 'departure_time', 'day']:
    dd_correlations[col] = df.select(corr('departure_delay', col)).collect()[0][0]
    #print(f"Correlation between departure_delay and {col}: {dd_correlations[col]}")
    
max(dd_correlations, key=dd_correlations.get)

# References
# https://www.google.com/search?q=find+key+with+max+value+python&rlz=1C1CHBF_enUS1071US1071&oq=find+key+with+max+value+&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBggBEEUYOTIHCAIQABiABDIICAMQABgWGB4yCAgEEAAYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yDQgHEAAYhgMYgAQYigUyDQgIEAAYhgMYgAQYigUyDQgJEAAYhgMYgAQYigXSAQg4NzU1ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
# https://www.google.com/search?q=how+to+find+correlation+coefficient+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=how+to+find+correlation+coefficient+pyspark&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDkzMDZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

### mp9 - 3.2.3.4

from pyspark.sql.functions import col, when

df_w_departure_time_bucket = df_no_dups.withColumn("DepartureTimeBucket", when(((col("departure_time")/ 100).cast('int') <= 5) & ((col("departure_time")/ 100).cast('int') <= 11), "Morning")
    .when(((col("departure_time")/ 100).cast('int') <= 12) & ((col("departure_time")/ 100).cast('int') <= 17), "Afternoon")
    .when((((col("departure_time")/ 100).cast('int') <= 18) & ((col("departure_time")/ 100).cast('int') <= 23)) | \
          ((((col("departure_time")/ 100).cast('int') <= 0) & ((col("departure_time")/ 100).cast('int') <= 4)) | ((col("departure_time")/ 100).cast('int') == 24)), "Night")
    .otherwise("Unknown"))

#df_w_departure_time_bucket.select('departure_time', 'DepartureTimeBucket').show(10)

df_w_departure_time_bucket.write.csv('s3://fridkis-mp9-flights-dataset/Transformed-Output/Glue-Job-3/', header=True, mode="overwrite")

