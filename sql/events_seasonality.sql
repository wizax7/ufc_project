SELECT 
    COUNT(*) AS events_count, 
    EXTRACT(MONTH FROM date) AS month 
FROM ufc_events 
GROUP BY month 
ORDER BY 2 ASC;