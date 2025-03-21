-- -- 3.3.3-1 -- --
--SELECT Airline, Origin_Airport, Destination_Airport, floor(departure_time/100) AS departure_hour
SELECT Airline, Origin_Airport, Destination_Airport
FROM " transformed-flights-data-3-glue_job_3"
WHERE floor(departure_time/100) >= 8.0 AND floor(departure_time/100) < 12.0
AND month = 12 AND day = 25
AND origin_airport = 'ORD';

-- -- 3.3.3-2 -- --
-- f1 is flight1; f2 is flight2
-- stop_over_time = f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + f1.time_zone_difference)

--SELECT DISTINCT Airline, Origin_Airport, Stopover_Airport, Destination_Airport, Origin_Departure_Delay, Stopover_Arrival_Delay, Stopover_Departure_Delay, Destination_Arrival_Delay, stop_over_time, f1_day, f2_day, tzd, f1_month, f2_month, f1_year, f2_year, f1dt, f2dt
SELECT DISTINCT Airline, Origin_Airport, Stopover_Airport, Destination_Airport, Origin_Departure_Delay, Stopover_Arrival_Delay, Stopover_Departure_Delay, Destination_Arrival_Delay
FROM 
(
    SELECT f1.Airline AS Airline, f1.Origin_Airport AS Origin_Airport, f1.Destination_Airport as Stopover_Airport, f2.Destination_Airport AS Destination_Airport, f1.departure_delay AS Origin_Departure_Delay, f1.Arrival_Delay AS Stopover_Arrival_Delay, f2.Departure_Delay AS Stopover_Departure_Delay, f2.Arrival_Delay as Destination_Arrival_Delay, (f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + f1.time_zone_difference)) AS stop_over_time, f1.time_zone_difference AS tzd, f1.day AS f1_day, f2.day AS f2_day, f1.month AS f1_month, f2.month AS f2_month, f1.year AS f1_year, f2.year AS f2_year, f1.departure_time as f1dt, f2.departure_time as f2dt
    --SELECT *, (f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + f1.time_zone_difference)) AS stop_over_time, f1.time_zone_difference
    FROM " transformed-flights-data-3-glue_job_3" AS f1, " transformed-flights-data-3-glue_job_3" AS f2
    WHERE f1.Origin_Airport = 'SFO'
    AND f2.Destination_Airport = 'JFK'
    AND f1.Destination_Airport = f2.Origin_Airport
    AND f1.Airline = f2.Airline
    AND f1.cancelled = 0 AND f2.cancelled = 0
    --AND (((f1.day = f2.day OR f1.day + 1 = f2.day) AND f1.month = f2.month AND f1.year = f2.year) OR
    --     ((f1.day = 28 OR f1.day = 29) AND f2.day = 1 AND f1.month = 2 AND f2.month = 3 AND f1.year = f2.year) OR
    --     (f1.day = 30 AND f2.day = 1 AND f1.month IN (4,6,9,11) AND f1.month + 1 = f2.month AND f1.year = f2.year) OR
    --     (f1.day = 31 AND f2.day = 1 AND f1.month IN (1,3,5,7,8,10) AND f1.month + 1 = f2.month AND f1.year = f2.year) OR
    --     (f1.day = 31 AND f2.day = 1 AND f1.month = 12 AND f2.month = 1 AND f1.year + 1 = f2.year))
) AS t1
WHERE 60 <= t1.stop_over_time AND t1.stop_over_time <= 180


-- -- 3.3.3-3 -- --
SELECT DepartureTimeBucket, ROUND(AVG(arrival_delay)) AS Average_Arrival_Delay FROM " transformed-flights-data-3-glue_job_3"
WHERE arrival_delay >= 0
GROUP BY (DepartureTimeBucket)

--SELECT departure_time, DepartureTimeBucket FROM " transformed-flights-data-3-glue_job_3"
--WHERE departure_time = 2400

--UPDATE " transformed-flights-data-3-glue_job_3"
--SET departuretimebucket = 'Night'
--WHERE departure_time = 2400
