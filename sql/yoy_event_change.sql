SELECT 
    year, 
    total_events, 
    prev_year_events, 
    ROUND((total_events - prev_year_events)::numeric / prev_year_events * 100, 2) AS yoy_change_pct
FROM (
    SELECT 
        EXTRACT(YEAR FROM date) AS year,
        COUNT(*) AS total_events, 
        LAG(COUNT(*)) OVER(ORDER BY EXTRACT(YEAR FROM date)) AS prev_year_events 
    FROM ufc_events
    GROUP BY year
    ORDER BY year
)
;