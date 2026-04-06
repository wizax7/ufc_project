SELECT
    SPLIT_PART(location, ',', 3) AS country, 
    COUNT(*) AS events_count
FROM ufc_events
WHERE SPLIT_PART(location, ',', 3) <> ''
GROUP BY country
ORDER BY events_count DESC;