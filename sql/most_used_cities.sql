SELECT 
	SPLIT_PART(location, ',', 1) AS city, 
	COUNT(*) AS events_count
FROM ufc_events 
WHERE SPLIT_PART(location, ',', 1) <> ''
GROUP BY city
ORDER BY events_count DESC
LIMIT 15;