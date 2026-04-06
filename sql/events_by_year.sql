SELECT 
    COUNT(*) AS events_count, 
    EXTRACT(YEAR FROM date) AS year
FROM ufc_events
GROUP BY year
ORDER BY 2 DESC;