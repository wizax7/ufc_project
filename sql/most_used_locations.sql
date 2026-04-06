SELECT 
    location, 
    COUNT(*) AS events_count
FROM ufc_events
GROUP BY location
HAVING COUNT(*) > 1
ORDER BY 2 DESC
LIMIT 20;