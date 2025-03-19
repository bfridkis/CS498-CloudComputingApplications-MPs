-- -- 3.3.1-1 -- --
--SELECT Airline, Origin_Airport, Destination_Airport, floor(departure_time/100) AS departure_hour
SELECT Airline, Origin_Airport, Destination_Airport
FROM " transformed-flights-data-3-glue_job_3"
WHERE floor(departure_time/100) >= 8.0 AND floor(departure_time/100) < 12.0
AND origin_airport = 'ORD';

-- -- 3.3.1-2 -- --
-- f1 is flight1; f2 is flight2
-- stop_over_time = f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + f1.time_zone_difference)

SELECT f1.Airline AS Airline, f1.Origin_Airport AS Origin_Airport, f2.Destination_Airport AS Destination_Airport, f1.departure_delay AS Origin_Departure_Delay, f1.Arrival_Delay AS Stopover_Arrival_Delay, f2.Departure_Delay AS Stopover_Departure_Delay, f2.Arrival_Delay as Destination_Arrival_Delay, (f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + f1.time_zone_difference)) AS stop_over_time, f1.time_zone_difference
FROM " transformed-flights-data-3-glue_job_3" AS f1, " transformed-flights-data-3-glue_job_3" AS f2
WHERE f1.Destination_Airport = f2.Origin_Airport
AND f1.Airline = f2.Airline
AND f1.time_zone_difference > 0
-- AND 60 <= stop_over_time AND stop_over_time <= 180
LIMIT 10