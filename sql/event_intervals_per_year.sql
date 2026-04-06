WITH event_intervals AS (
	SELECT 
		EXTRACT(YEAR FROM date) AS year,
		date, 
		LAG(date) OVER(ORDER BY date ASC) AS prev_date
	FROM ufc_events
)

SELECT 
	year,
	COUNT(*) AS events_in_year,
	MIN(date - prev_date) AS min_days, 
	MAX(date - prev_date) AS max_days, 
	ROUND(AVG(date - prev_date), 2) AS avg_days
FROM event_intervals
WHERE prev_date IS NOT NULL
GROUP BY year
ORDER BY year
;